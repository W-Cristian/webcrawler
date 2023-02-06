from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# import sys
# sys.path.append('/app/utilities')
# from logger import mylogger

def Generate_browser():

    # browser = webdriver.Remote(command_executor='http://selenium:4444/wd/hub',
    #     desired_capabilities=DesiredCapabilities.FIREFOX)
    # options = DesiredCapabilities.FIREFOX
    # options["maxInstances"]= 5
    # mylogger.info(options)

    _browser = webdriver.Remote(command_executor='https://coduct-crawler-selenium.braveforest-44e154a2.westeurope.azurecontainerapps.io/wd/hub',
        desired_capabilities=DesiredCapabilities.FIREFOX)
    return _browser