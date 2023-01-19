from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def Generate_browser():
    browser = webdriver.Remote(command_executor='http://selenium:4444/wd/hub',
        desired_capabilities=DesiredCapabilities.FIREFOX)
    return browser