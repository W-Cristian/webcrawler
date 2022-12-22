from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time

def RedirectPage(searchhWord):
    url = "http://www.freelance.de/"
    time.sleep(5)
    browser = webdriver.Remote('http://selenium:4444/wd/hub',
        desired_capabilities=DesiredCapabilities.CHROME)
    browser.get(url)
    time.sleep(2)
    # browser.save_screenshot('screenshot.png')

    search_el = browser.find_element(By.ID, 'search-text')
    search_el.send_keys(searchhWord)
    time.sleep(2)

    submit_btn_el = browser.find_element(By.XPATH, "//button[@class='btn btn-primary'][@type='button']")
    submit_btn_el.click()
    time.sleep(2)
    return browser

def TakeInfo (browser,quantity=None):
    divBox = browser.find_elements(By.XPATH, "//div[@class='list-item-main']")
    if quantity is not None:
        index = range(0,quantity)
    else:
        index = range(0, len(divBox))
    propositions = []
    for i in index:
        header = divBox[i].find_element(By.CSS_SELECTOR, "h3")
        link = header.find_element(By.CSS_SELECTOR, "a").get_attribute('href')
        print(header.text)
        print(link)
        firma = divBox[i].find_element(By.CLASS_NAME , 'company-name').text
        print(firma)
        print()
        details = divBox[i].find_element(By.CLASS_NAME , 'icon-list')
        details_array = []
        detail = details.find_elements(By.CSS_SELECTOR, "li")
        detail
        for detail in details.find_elements(By.CSS_SELECTOR, "li"):
            details_array.append(detail.text)

        obj = {
        "header" : header.text,
        "firma" : firma,
        "details" : details_array,
        "link" : link
        }     
        propositions.append(obj)
    browser.quit()
    return propositions

def ReturnData(searchhWord,oferts,quantity=None):
    file_data = dict({"Key": searchhWord,
    "quantity": quantity,
        "data":[]})
    file_data["data"] = oferts
    return file_data

# searchhWord = ".net"

# browser = RedirectPage(searchhWord)
# oferts = TakeInfo (browser)
# data = ReturnData(searchhWord,oferts)