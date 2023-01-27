import sys
sys.path.append('/app/utilities')
from logger import mylogger
from selenium.webdriver.common.by import By
import time

def Redirect_page(searchWord,browser):
    url = f"https://www.hays.de/jobsuche/stellenangebote-jobs/j/Contracting/3/p/1?q={searchWord}"
    time.sleep(2)
    mylogger.debug(f"searchword -----{searchWord}")
    browser.get(url)
    time.sleep(2)

    return browser

def Make_list (browser):
    divBox = browser.find_elements(By.XPATH, "//div[@class='search__result']")
    index = range(0, len(divBox))
    propositions = []
    print (len(divBox))
    for i in index:
        
        link = divBox[i].find_element(By.CSS_SELECTOR, "a")

        details_array = []
        list_elements = divBox[i].find_elements(By.CLASS_NAME, "info-text")
        for info_text in list_elements:
            details_array.append(info_text.text)
        
        details_with_label ={}
        details_with_label["place"] = details_array[0]
        details_with_label["type"] = details_array[1]
        details_with_label["startdatum"] = details_array[2]

        prospectnumber = divBox[i].find_element(By.XPATH, ".//div[@class='search__result__prospectnumber']").text
        teaser = divBox[i].find_element(By.XPATH, ".//div[@class='search__result__teaser']").text
        
        obj = {
        "header" : link.text,
        "prospectnumber" : prospectnumber,
        "teaser" : teaser,
        "details" : details_with_label,
        "link" : link.get_attribute('href')
        }     
        mylogger.debug("-- links - {} ...".format(obj["link"]))
        propositions.append(obj)
    mylogger.debug("taken -{}- links ...".format(len(propositions)))
    return propositions

def Take_info (browser,data,quantity=None):
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
        task_array = ""
        try:
            tasks =  browser.find_element(By.CLASS_NAME, "hays__job__detail__your-task")
            details = tasks.find_elements(By.CSS_SELECTOR, "li")
            for i in details:
                task_array = task_array + i.text + "| "
            task_array = task_array[:-2]
        except Exception as err:
            task_array = None
            mylogger.debug("EXPETED ERROR -{err}")

        competences_array = ""
        try:
            competences =  browser.find_element(By.CLASS_NAME, "hays__job__details__your-qualifications")
            details = competences.find_elements(By.CSS_SELECTOR, "li")
            for i in details:
                competences_array =competences_array + i.text + "| "
            competences_array = competences_array[:-2]
        except Exception as err:
            competences_array = None
            mylogger.debug("EXPETED ERROR -{err}")

        advantages_array = ""
        try: 
            advantages =  browser.find_element(By.CLASS_NAME, "hays__job__details__your-advantages")
            details = advantages.find_elements(By.CSS_SELECTOR, "li")
            for i in details:
                advantages_array = advantages_array + i.text + "| "
            advantages_array = advantages_array[:-2]
        except Exception as err:
            advantages_array = None
            mylogger.debug("EXPETED ERROR -{err}")

        contact_holder =  browser.find_element(By.CLASS_NAME, "hays__job__details__your-contact-at-hays")
        details = contact_holder.find_elements(By.CSS_SELECTOR, "a")
        telefon = ""
        mail = ""
        for i in details:
            if "mailto:" in i.get_attribute('href'):
                if mail == "":
                    mail = i.text
            if "callto:" in i.get_attribute('href'):
                telefon = i.get_attribute('href').replace("callto:","")
        contact = {}
        contact["mail"] = mail
        contact["telefon"] = telefon
        name_el =  browser.find_element(By.CLASS_NAME, "hays__job__details__your-contact-at-hays__item")
        if "Mein Ansprechpartner" in name_el.text:
            contact["name"] = name_el.text.replace("Mein Ansprechpartner\n","")        
                
        description = {}
        description["tasks"] = task_array
        description["advantages"] = advantages_array
        description["competences"] = competences_array

        obj = {
        "header" : data[x]["header"],
        "prospectnumber" : data[x]["prospectnumber"].replace("Referenznummer: ",""),
        "description" : description,
        "details" : data[x]["details"],
        "contact" : contact,
        "link" : data[x]["link"]
        }     
        propositions.append(obj)

    return propositions

def Return_data(searchWord,oferts):
    file_data = dict({"Key": searchWord,
    "quantity": len(oferts),
        "data":[]})
    file_data["data"] = oferts
    return file_data