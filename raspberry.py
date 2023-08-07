import requests
import time
import subprocess
import re
import statistics

# Replace with your Wi-Fi SSID and password
ssid = "YOURSSIDHERE"
password = "WIFIPASSWORDHERE"

# Replace with your server URL or IP address
server_url = "http://192.168.1.237:5000"

# Replace with the correct Wi-Fi interface name
interface = "wlan1"

# Global variables for Wi-Fi jamming detection
window_size = 10
moving_average_window = []

# Global variable for the number of standard deviations for the threshold
threshold_multiplier = 1

def connect_to_wifi(ssid, password):
    print("Connecting to WiFi...")
    # Replace this section with your actual code to connect to Wi-Fi
    # For example, using NetworkManager or other Wi-Fi management tools.
    time.sleep(1)  # Simulating the connection process, adjust this time as needed
    print("Connected to WiFi")

def send_wifi_data_to_server(ssid, address, rssi):
    try:
        response = requests.post(
            f"{server_url}/save",
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data={'ssid': ssid, 'address': address, 'rssi': rssi}
        )

        if response.status_code == 200:
            print(response.text)
        else:
            print(f"Error on sending POST: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending Wi-Fi data to server: {e}")

def send_jamming_alert_to_server(timestamp, current_strength, moving_avg):
    data = {
        'timestamp': timestamp,
        'current_strength': current_strength,
        'moving_avg': moving_avg,
    }
    try:
        response = requests.post(f"{server_url}/jamming_alert", json=data)
        if response.status_code == 200:
            print("Jamming alert sent to server successfully")
        else:
            print(f"Error on sending jamming alert to server: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending jamming alert to server: {e}")

def get_signal_strength(interface):
    try:
        # Run the iw command to get the signal strength
        output = subprocess.check_output(["iw", interface, "link"]).decode()
        print("IW Output:")
        print(output)

        # Extract the signal strength from the output
        match = re.search(r"signal: (-?\d+) dBm", output)
        if match:
            return int(match.group(1))
        else:
            print("Could not extract signal strength.")
            return None
    except Exception as e:
        print(f"Error getting signal strength: {e}")
        return None

def scan_wifi():
    print("Scanning networks...")
    try:
        scan_output = subprocess.check_output(["sudo", "iwlist", interface, "scan"]).decode("utf-8")
        print("Scan Output:")
        print(scan_output)

        networks = parse_scan(scan_output)

        if len(networks) == 0:
            print("No networks found")
        else:
            print(f"{len(networks)} networks found")
            for i, network in enumerate(networks):
                print(f"{i + 1}: {network['ssid']} ({network['rssi']})")
                send_wifi_data_to_server(network['ssid'], network['address'], network['rssi'])
                time.sleep(0.01)

        time.sleep(1)
    except subprocess.CalledProcessError as e:
        print(f"Error scanning networks: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def parse_scan(scan_output):
    lines = scan_output.split("\n")
    networks = []
    network = {}

    for line in lines:
        if "Cell" in line and network:
            networks.append(network)
            network = {}
        if "ESSID:" in line:
            network['ssid'] = line.split('ESSID:"')[1].split('"')[0]
        if "Address: " in line:
            network['address'] = line.split('Address: ')[1]
        if "Signal level=" in line:
            network['rssi'] = re.findall(r"Signal level=(-?\d+)", line)[0]

    if network:
        networks.append(network)

    return networks

def get_visible_wifi_networks_count():
    try:
        result = subprocess.check_output(['iwlist', 'wlan0', 'scan'])
        visible_networks_count = result.decode('utf-8').count('ESSID')
        return visible_networks_count
    except:
        return 0

def get_packet_loss_to_gateway():
    try:
        result = subprocess.check_output(['ping', '-c', '4', '192.168.1.1'])
        packet_loss_line = [line for line in result.decode('utf-8').split('\n') if 'packet loss' in line][0]
        packet_loss = int(packet_loss_line.split('%')[0].split()[-1])
        return packet_loss
    except:
        return 100

def main():
    try:
        connect_to_wifi(ssid, password)
        min_strength = 1000  # start with a high value

        while True:
            current_strength = get_signal_strength(interface)
            
            if current_strength is not None:
                min_strength = min(min_strength, current_strength)
                print(f"Current Signal Strength: {current_strength} dBm")

                moving_average_window.append(current_strength)
                if len(moving_average_window) > window_size:
                    moving_average_window.pop(0)

                moving_avg = sum(moving_average_window) / len(moving_average_window)
                print(f"Moving Average: {moving_avg:.2f} dBm")

                send_continuous_update(current_strength, moving_avg)  # Separate function for clarity

                # Check for jamming immediately
                if check_for_jamming(current_strength, moving_avg):  # Returns True if jamming detected
                    continue  # Skip the rest of the loop and start next iteration

                scan_wifi()
                time.sleep(2)  # Reduced sleep time
            else:
                print("Signal strength not available")

    except KeyboardInterrupt:
        print("Jammer stopped")

def send_continuous_update(current_strength, moving_avg):
    data = {
        'current_strength': current_strength,
        'moving_avg': moving_avg,
    }
    try:
        response = requests.post(f"{server_url}/continuous_update", json=data)
        if response.status_code == 200:
            print("Continuous update sent to server successfully")
        else:
            print(f"Error on sending continuous update to server: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending continuous update to server: {e}")

def check_for_jamming(current_strength, moving_avg):
    if len(moving_average_window) < 2:
        print("Not enough data points for jamming detection.")
        return False

    std_dev = statistics.stdev(moving_average_window)
    threshold = moving_avg - (threshold_multiplier * std_dev)

    if current_strength < threshold:
        print("Jamming detected!")
        timestamp = int(time.time())
        send_jamming_alert_to_server(timestamp, current_strength, moving_avg)
        return True
    else:
        print("No jamming detected")
        return False

if __name__ == "__main__":
    main()
