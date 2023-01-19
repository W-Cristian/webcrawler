import sys
sys.path.append('/app/utilities')
from logger import mylogger
from selenium.webdriver.common.by import By
import time
from .general_resources import Generate_browser


import json

def RedirectPage(searchWord):
    url = "https://www.solcom.de/de/projektportal"
    browser = Generate_browser()
    time.sleep(2)
    browser.get(url)
    time.sleep(2)

    search_el = browser.find_element(By.ID, 'stichwort')
    search_el.send_keys(searchWord)
    try:
        cookies = browser.find_element(By.CLASS_NAME, 'allow-essential-only')
        cookies.click()
        time.sleep(2)
    except:
        mylogger.debug("no ask for cookies")
    search_el.submit()
    time.sleep(3)
    return browser


def Make_list (browser):
    divBox = browser.find_elements(By.XPATH, "//div[@class='contenance-solcom-portal-project-item project-item']")
    index = range(0, len(divBox))
    propositions = []

    for i in index:
    
        link = divBox[i].find_element(By.CSS_SELECTOR, "a")
        
        projectNr = divBox[i].find_element(By.XPATH, ".//div[@class='project-header']//div")
        obj = {
        "header" : link.get_attribute('data-projectname'),
        "link" : link.get_attribute('href'),
        "prospectnumber" : projectNr.text.replace("Projekt-Nr.: ","")
        }    
        propositions.append(obj)
    mylogger.debug("taken -{}- links ...".format(len(propositions)))

    return propositions

def TakeInfo (browser,data,quantity=None):
    if quantity is not None and len(data)>quantity:
        index = range(0,quantity)
    else:
        index = range(0, len(data))
        
    propositions = []
    count = 0
    for x in index:

        count=count+1
        mylogger.debug("taking details from -{}- link: {}".format(count,data[x]["link"]))

        browser.get(data[x]["link"])
        time.sleep(2)
        container =  browser.find_element(By.CLASS_NAME, "projectdetail-container")
        description_container = container.find_element(By.XPATH, ".//div[@class='neos-nodetypes-text projekt-desc']")
        lists = description_container.find_elements(By.CSS_SELECTOR, "ul")

        details = container.find_elements(By.XPATH, ".//div[@class='project-infos']//li//span[@class='icon-value']")
        detailsobj = {
            "Dauer" : details[0].text,
            "Starttermin" : details[1].text,
            "Einsatzort" : details[2].text,
            "Stellentyp" : details[3].text,
        }
        paragraphs = description_container.find_elements(By.CSS_SELECTOR, "p")
        
        description = description_container.text
        description = description.replace(paragraphs[0].text,"").replace(paragraphs[2].text,"").replace("Zusätzliche Informationen:","")
    #         paragraph = paragraphs[1].text

    #         lists = description_container.find_elements(By.CSS_SELECTOR, "ul")
    #         tasks = lists[0].find_elements(By.CSS_SELECTOR, "li")
    #         task_array = ""
    #         for i in tasks:
    #             task_array = task_array + i.text + "|"

    #         competences = lists[1].find_elements(By.CSS_SELECTOR, "li")
    #         competences_array = ""
    #         for i in competences:
    #             competences_array = competences_array + i.text + "|"
            # solcom = Solcom(data[x]["header"],description,data[x]["prospectnumber"],detailsobj,data[x]["link"])
        obj = {
        "header" : data[x]["header"],
        "description" : description,
        "prospectnumber" : data[x]["prospectnumber"],
#         "tasks" : task_array[:-1],
#         "competences" : competences_array[:-1],
        "details" : detailsobj,
        "link" : data[x]["link"]
        }     
        propositions.append(obj)

    return propositions

# class Solcom:

#     def __init__(self, header, description,prospectnumber,details,link):
#         self.header = header
#         self.description = description
#         self.prospectnumber = prospectnumber
#         self.details = details
#         self.link = link
#     def Json(self):
#         return json.dumps(self.__dict__)