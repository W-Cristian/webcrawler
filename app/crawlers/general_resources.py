from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options
import sys
sys.path.append('/app/utilities')
from logger import mylogger
import os
SELENIUM_HUB = os.environ.get('SELENIUM_HUB')

class seleniumConection:
    def __init__(self):
        remote_url = SELENIUM_HUB + '/wd/hub'
        self._browser = webdriver.Remote(command_executor=remote_url,
            desired_capabilities=DesiredCapabilities.FIREFOX)

    def browser(self):
        return self._browser

def Generate_browser():

    selenuim_instance = seleniumConection()
    return selenuim_instance.browser()