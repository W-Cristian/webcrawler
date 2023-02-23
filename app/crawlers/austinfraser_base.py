import sys
sys.path.append('/app/utilities')
from logger import mylogger
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

def Redirect_page(searchWord,browser):
    url = f"https://www.austinfraser.com/de/jobangebote?query={searchWord}&selected_locations=2921044"
    try:
        browser.get(url)
    except Exception as e:
        mylogger.error('HP error ')
        mylogger.error(e)
        raise e
    return browser

def Make_list (browser):
    try:
        element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//li[@class='job-result-item']"))
            )
    except Exception as e:
        mylogger.error(e)
        raise e

    divBox = browser.find_elements(By.XPATH, "//li[@class='job-result-item']")
    index = range(0, len(divBox))
    propositions = []
    time.sleep(1)

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
    try:
        element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//ul[@class='format clearfix']"))
            )
    except Exception as e:
        mylogger.error(e)
        raise e

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
        try:
            element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.ID, "extra-info"))
                )
        except Exception as e:
            mylogger.error(e)
            raise e
        container =  browser.find_element(By.ID, "extra-info")
        details = container.find_elements(By.XPATH, ".//li")
        detailsobj = {}
        for detail in details:
            value = detail.find_element(By.XPATH, ".//span").text.strip()
            detailsobj[detail.text.rstrip(value).strip('\n')]=value
        
        description =  browser.find_element(By.XPATH, "//div[@class='wrapper body']").text
        
        contact_block =  browser.find_element(By.ID, "job-consultant-block")
        try:
            link =  contact_block.find_element(By.CSS_SELECTOR, "a").get_attribute('href')
            contact = Take_contact(browser,link)
        except:
            mylogger.info(f"EXPECTED ERROR - NOT FOUND .job-consultant-block.a")
            contact = Take_contact(browser,None)

        contact["name"] = ""
        if "Kontakt" in detailsobj:
            contact["name"] = detailsobj["Kontakt"]
        prospectnumber = ""
        if "Job-Referenz" in detailsobj:
            prospectnumber = detailsobj["Job-Referenz"]

        obj = {
        "header" : data[x]["header"],
        "contact" : contact,
        "description" : description,
        "prospectnumber" : prospectnumber,
        "details" : detailsobj,
        "link" : data[x]["link"]
        }     
        propositions.append(obj)
    return propositions