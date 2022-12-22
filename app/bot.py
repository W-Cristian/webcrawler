from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time

url = "https://www.freelance.de"
time.sleep(5)

driver = webdriver.Remote('http://selenium:4444/wd/hub',
    desired_capabilities=DesiredCapabilities.CHROME)
driver.get(url)
time.sleep(5)
driver.save_screenshot('screenshot.png')