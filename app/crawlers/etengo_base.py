import sys
sys.path.append('/app/utilities')
from logger import mylogger
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

import requests
import json

def Make_list(searchWord):
    url = f'https://www.etengo.de/?action=etengo%2Fproject%2Ffilter&zip=&branch=&text={searchWord}'
    respose = requests.request('GET',url, data="",headers={})
    data = json.loads(respose.text)
    propositions=[]
    
    for i in data["items"]:
        index_href = i.index('href="')
        end_index_href = i.index('"',index_href+7)
        href= i[index_href+6: end_index_href]
        index_title = i.index('title="')
        end_index_title = i.index('"',index_title+8)
        title= i[index_title+7: end_index_title]
        obj = {
            "header" : title,
            "link" : href,
            }    
        propositions.append(obj)
    mylogger.info("taken -{}- links ...".format(len(propositions)))

    return propositions

def Take_info (browser,data,quantity=None):
    if quantity is not None and len(data)>quantity:
        index = range(0,quantity)
    else:
        if len(data) < 20:
            index = range(0, len(data))
        else:
            index = range(0, 20)
        
    count = 0
    propositions = []

    for i in index:

        count=count+1
        mylogger.info(f"taking details from -{count}- link: {data[i]['link']}")
        try:
            browser.get(data[i]["link"])
            element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//article[@class='node clearfix node-rt-box']"))
            )
        except Exception as e:
            mylogger.error('HP error ')
            mylogger.error(e)
            raise e

        container = browser.find_element(By.XPATH, "//article[@class='node clearfix node-rt-box']")
        description = container.find_element(By.XPATH, ".//div").text

        details = container.find_elements(By.XPATH, ".//div[@class='jobinfos']//dd")
        label_details = container.find_elements(By.XPATH, ".//div[@class='jobinfos']//dt")
        detailsobj = {}
        index = 0
        for detail in details:
            if index == len(details)-1:
                continue
            detailsobj[label_details[index].text] = details[index].text
            index=index+1

        contact_block =  details[-1].text.split("\n")
        contact = {
            "name" : contact_block[0],
            "mail" : contact_block[1]
        }

        obj = {
        "header" : data[i]["header"],
        "contact" : contact,
        "description" : description,
        "prospectnumber" : detailsobj["CA-Nummer"],
        "details" : detailsobj,
        "link" : data[i]["link"]
        }     
        propositions.append(obj)
    return propositions