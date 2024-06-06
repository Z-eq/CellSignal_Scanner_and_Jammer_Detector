
# Cell Tracker and Jammer Detection 

This is a Wi-Fi jammer detection application designed to monitor and detect potential Wi-Fi jamming events, it is also wifi scanner and can be made to cellphone tracker sniffing for ssid/mac addresses of cellphones. The application runs on a Raspberry Pi and continuously scans nearby Wi-Fi networks, calculates moving averages, and sends Wi-Fi signal data to a server for analysis. When potential jamming is detected, alerts are sent to the server.

## Features

- Continuously monitor Wi-Fi signal strength and moving averages.
- Send continuous updates to the server for analysis.
- Detect potential jamming based on multiple thresholds (warning and alert levels).
- Monitor the number of visible Wi-Fi networks as an additional indicator.
- Monitor packet loss using ping tests.
- Send alerts to the server when jamming is detected.
- Display the latest jamming events and their details on a web interface.

## Requirements

- Raspberry Pi with Wi-Fi capabilities or any device with Linux ( Have not tested on windows but i think it will run on it aswell).
- Python 3 and the following Python packages:
  - requests
  - time
  - subprocess
  - re
  - statistics
- Flask and Flask-SocketIO for the web interface.
- A server to receive and analyze Wi-Fi signal data.

- It is built using Python and utilizes the pcapy library for efficient Wi-Fi signal monitoring. Alternatively, you could use the more comprehensive scapy library   to access higher-level functionalities related to network packet manipulation.

## Installation

1. Clone the repository to your Raspberry Pi.
2. Install the required Python packages using pip:
   ```
   pip install requests Flask Flask-SocketIO
   ```
3. Set up the Flask app on your server. Refer to `app.py` for the Flask app code.
4. Run the application on your Raspberry Pi:
   ```
   sudo python3 raspbery.py
   ```

## Configuration

- Modify the `ssid` and `password` variables in `raspbery.py` to match your Wi-Fi network.
- Change the `server_url` variable to your server's URL or IP address.
- Adjust the `threshold_multiplier` and other threshold values in `raspbery.py` to suit your detection requirements.

## Usage

1. Run the application on your Raspberry Pi using the command provided in the installation step.
2. The application will start scanning nearby Wi-Fi networks and send the data to the server.
3. The web interface on the server will display the live signal strength and moving average.
4. When potential jamming is detected, alerts will be sent to the server and displayed on the web interface.
5. The latest jamming events and their details will be shown on the web interface.

## Note

- This application is designed for educational and testing purposes only.
- Jamming detection is based on signal strength, moving averages, visible networks, and packet loss, but false positives or negatives are possible.
- Adjust threshold values and other parameters based on your environment and requirements.


**Planned Enhancements:**

1. **Integration of SDR Devices:** We are actively working on integrating Software Defined Radio (SDR) devices to scan for jamming signals over a wider range of frequencies. SDR allows us to access and analyze radio signals in real-time, making it possible to detect various types of interference and unauthorized transmission attempts.

2. **Advanced Jamming Detection Techniques:** With the help of SDR, we will implement advanced jamming detection techniques to identify more sophisticated and elusive jamming attempts. These techniques may include signal modulation analysis, signal fingerprinting, and pattern recognition.

3. **Jamming Countermeasures:** In addition to detection, we aim to develop effective countermeasure techniques to mitigate the impact of jamming attacks on Wi-Fi networks. These countermeasures will be designed to dynamically adapt to the type of jamming signal encountered and take appropriate action to maintain network connectivity.

4. **User-Friendly Interface:** We plan to create a user-friendly interface to configure the application, view real-time signal metrics, and manage countermeasure settings. The interface will allow users to easily monitor and control the system.

5. **Centralized Monitoring and Reporting:** We intend to enable centralized monitoring and reporting by integrating the application with a central management system. This will provide network administrators with a comprehensive view of Wi-Fi signal health and jamming events across multiple locations.

**Important Notes:**

- Integrating SDR devices and implementing countermeasures require advanced expertise in radio frequency analysis and network security. We are committed to conducting extensive testing and validations to ensure the effectiveness and safety of the techniques used.

- The application's jamming detection and countermeasure features are subject to ongoing development and improvements. We encourage user feedback and contributions to enhance the overall reliability and performance of the application.

**Contributing:**

Contributions to this project are welcome! If you have expertise in SDR, network security, or software development, your contributions can significantly contribute to the success of this project. Feel free to open issues, share ideas, or submit pull requests to collaborate with us.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

This application was developed as part of a Wi-Fi jamming detection project for educational purposes. We acknowledge the contributions of the open-source community and developers of the Python packages used in this project.

## Contact

For questions or feedback, please contact [zeq.alidemaj@gmail.com](mailto:zeq.alidemaj@gmail.com).
