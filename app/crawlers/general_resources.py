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
        # options = Options() 
        # options.to_capabilities().timeouts
        self._browser = webdriver.Remote(command_executor='http://selenium:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.FIREFOX)

        # self._browser = webdriver.Remote(command_executor='https://coduct-crawler-selenium.braveforest-44e154a2.westeurope.azurecontainerapps.io/wd/hub',
        # desired_capabilities=DesiredCapabilities.FIREFOX)
        # self._browser = webdriver.Remote(command_executor='https://coduct-crawler-selenium.braveforest-44e154a2.westeurope.azurecontainerapps.io/wd/hub',
        #   desired_capabilities=DesiredCapabilities.FIREFOX)
        # self._browser = webdriver.Remote(command_executor='https://selenium-app-web.azurewebsites.net//wd/hub',
        #     desired_capabilities=DesiredCapabilities.FIREFOX)
        # driver2 = webdriver.Remote(command_executor=the_known_url)  
        # self._browser.caps.timeouts.pageLoad
        # self._browser.set_page_load_timeout(60)
        # mylogger.info(f"timeouts - {self._browser.caps.timeouts}")
        
        # mylogger.info(f"browser - {self._browser.__dict__}")
        # mylogger.info(f"options - {options.__dict__}")
        # self._browser.SET_TIMEOUTS(60000)


    def browser(self):
        return self._browser

def Generate_browser():

    selenuim_instance = seleniumConection()
    return selenuim_instance.browser()