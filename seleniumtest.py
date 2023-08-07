from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import time

# Set up Selenium
# Replace '/path/to/chromedriver' with the actual path to your chromedriver
driver = webdriver.Chrome(service=Service('/chromedriver'))
driver.get('http://192.168.1.237:5000/jammer')

# Post a jamming alert
response = requests.post('http://192.168.1.237:5000/jamming_alert', json={
    "timestamp": time.time(),
    "current_strength": -80,
    "moving_avg": -30,
    "packet_loss_avg": 0.2
})

print(f"Posted jamming alert, received status code: {response.status_code}")

# Wait for the jammer page to update
element = WebDriverWait(driver, 30).until(
    EC.visibility_of_element_located((By.ID, 'jamming-alert'))  # Wait for the element to be visible
)

print(f"Element found: {element}")

# Verify that the jamming alert is displayed on the jammer page
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
alert = soup.find(id='jamming-alert')
assert alert is not None

print("Jamming alert is visible on the jammer page")

time.sleep(30)  # Keep the browser open for 30 seconds

driver.quit()  # Then close it

