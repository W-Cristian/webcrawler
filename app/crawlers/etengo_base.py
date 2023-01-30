import sys
sys.path.append('/app/utilities')
from logger import mylogger
from selenium.webdriver.common.by import By
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
        browser.get(data[i]["link"])
        time.sleep(2)
        container = browser.find_element(By.XPATH, "//article[@class='node clearfix node-rt-box']")
        description = container.find_element(By.XPATH, ".//div").text

        details = container.find_elements(By.XPATH, ".//div[@class='jobinfos']//dd")

        detailsobj = {
            "last_update" : details[0].text,
            "start" : details[1].text,
            "duration" : details[2].text,
            "Branche" : details[4].text,
            "workload" : details[5].text,
            "prospectnumber" : details[6].text,
        }

        contact_block =  details[7].text.split("\n")
        contact = {
            "name" : contact_block[0],
            "mail" : contact_block[1]
        }

        obj = {
        "header" : data[i]["header"],
        "contact" : contact,
        "description" : description,
        "prospectnumber" : detailsobj["prospectnumber"],
        "details" : detailsobj,
        "link" : data[i]["link"]
        }     
        propositions.append(obj)
    return propositions