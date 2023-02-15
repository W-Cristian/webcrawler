from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options
import sys
sys.path.append('/app/utilities')
from logger import mylogger
import os
SELENIUM_HUB = os.environ.get('SELENIUM_HUB')
WAITING_TIME = os.environ.get('WAITING_TIME')
import time

class seleniumConection:
    def __init__(self):
        remote_url = SELENIUM_HUB + '/wd/hub'
        self._browser = webdriver.Remote(command_executor=remote_url,
            desired_capabilities=DesiredCapabilities.FIREFOX,keep_alive=True)

    def browser(self):
        return self._browser

def Generate_browser():

    selenuim_instance = seleniumConection()
    #this time prevent the webdriver to crash because internet latency
    time.sleep(int(WAITING_TIME))
    return selenuim_instance.browser()

def Recover_session(session_id):
    remote_url = SELENIUM_HUB + '/wd/hub'
    browser = webdriver.Remote(command_executor=remote_url,
            desired_capabilities=DesiredCapabilities.FIREFOX,keep_alive=True)
    time.sleep(2)
    browser.session_id = session_id
    return browser
