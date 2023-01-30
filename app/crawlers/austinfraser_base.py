import sys
sys.path.append('/app/utilities')
from logger import mylogger
from selenium.webdriver.common.by import By
import time


import json

def Redirect_page(searchWord,browser):
    url = f"https://www.austinfraser.com/de/jobangebote?query={searchWord}&selected_locations=2921044"
    time.sleep(2)
    browser.get(url)
    time.sleep(2)
    return browser

def Make_list (browser):
    divBox = browser.find_elements(By.XPATH, "//li[@class='job-result-item']")
    index = range(0, len(divBox))
    propositions = []

    for i in index:
    
        link = divBox[i].find_element(By.CSS_SELECTOR, "a")
        
        obj = {
        "header" : link.get_attribute('text'),
        "link" : link.get_attribute('href'),
        }    
        propositions.append(obj)
    mylogger.info("taken -{}- links ...".format(len(propositions)))
    return propositions

def Take_contact(browser,contact_url):
    
    if contact_url == None:
        return  {
            "telephone" : None,
            "mail" : None,
            "Linkedin" : None
        }

    browser.get(contact_url)
    time.sleep(2)

    contact_block =  browser.find_elements(By.XPATH, "//ul[@class='format clearfix']//li")
    full_contact = {
        "telephone" : contact_block[0].find_element(By.CSS_SELECTOR, "a").get_attribute('href').strip("tel:"),
        "mail" : contact_block[1].find_element(By.CSS_SELECTOR, "a").get_attribute('href').replace("mailto:",""),
        "Linkedin" : contact_block[2].find_element(By.CSS_SELECTOR, "a").get_attribute('href'),
    }
    return full_contact

def Take_info (browser,data,quantity=None):
    if quantity is not None and len(data)>quantity:
        index = range(0,quantity)
    else:
        index = range(0, len(data))
        
    count = 0
    propositions = []

    for x in index:

        count=count+1
        mylogger.info(f"taking details from -{count}- link: {data[x]['link']}")
        browser.get(data[x]["link"])
        time.sleep(2)
        container =  browser.find_element(By.ID, "extra-info")
        details = container.find_elements(By.XPATH, ".//li//span")

        detailsobj = {
            "Salary" : details[0].text,
            "Sector" : details[1].text,
            "prospectnumber" : details[2].text,
            "Published" : details[4].text,
        }
        contact_name = details[3].text
        description =  browser.find_element(By.XPATH, "//div[@class='wrapper body']").text
        
        contact_block =  browser.find_element(By.ID, "job-consultant-block")
        try:
            link =  contact_block.find_element(By.CSS_SELECTOR, "a").get_attribute('href')
            contact = Take_contact(browser,link)
        except:
            mylogger.info(f"EXPECTED ERROR - NOT FOUND .job-consultant-block.a")
            contact = Take_contact(browser,None)

        contact["name"] = contact_name
        
        obj = {
        "header" : data[x]["header"],
        "contact" : contact,
        "description" : description,
        "prospectnumber" : detailsobj["prospectnumber"],
        "details" : detailsobj,
        "link" : data[x]["link"]
        }     
        propositions.append(obj)
    return propositions