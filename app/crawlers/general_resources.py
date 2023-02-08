from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options
import sys
sys.path.append('/app/utilities')
from logger import mylogger

class seleniumConection:
    def __init__(self):
        # mylogger.info(options)

        # self._browser = webdriver.Remote(command_executor='http://selenium:4444/wd/hub',
        # desired_capabilities=DesiredCapabilities.FIREFOX) 

        # self._browser = webdriver.Remote(command_executor='https://coduct-crawler-selenium.braveforest-44e154a2.westeurope.azurecontainerapps.io/wd/hub',
        # desired_capabilities=options)

        self._browser = webdriver.Remote(command_executor='https://coduct-crawler-selenium.braveforest-44e154a2.westeurope.azurecontainerapps.io/wd/hub',
          desired_capabilities=DesiredCapabilities.FIREFOX)
        self._browser.SET_TIMEOUTS(60000)
        mylogger.info(self._browser)


    def browser(self):
        return self._browser

def Generate_browser():

    selenuim_instance = seleniumConection()
    return selenuim_instance.browser()