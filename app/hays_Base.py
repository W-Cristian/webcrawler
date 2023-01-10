from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from logger import mylogger

def RedirectPage(searchWord):
    url = f"https://www.hays.de/jobsuche/stellenangebote-jobs/j/Contracting/3/p/1?q={searchWord}"
    browser = webdriver.Remote(command_executor='http://selenium:4444/wd/hub',
        desired_capabilities=DesiredCapabilities.FIREFOX)
    time.sleep(2)
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

def TakeInfo (browser,data,quantity=None):
    if quantity is not None:
        index = range(0,quantity)
    else:
        index = range(0, len(data))
        
    propositions = []
    count = 0

    for x in index:
        count=count+1
        mylogger.debug("taking details from -{}- link: {}".format(count,data[x]["link"]))

        try:
            browser.get(data[x]["link"])
            time.sleep(2)
            # if "status 400" in browser.title.lower():
            #     mylogger.debug("Not Posible To Load -{}- link {}".format(count,data[x]["link"]))
            #     count=count+1
            #     continue
            tasks =  browser.find_element(By.CLASS_NAME, "hays__job__detail__your-task")
            details = tasks.find_elements(By.CSS_SELECTOR, "li")
            task_array = []
            for i in details:
                task_array.append(i.text)

            competences =  browser.find_element(By.CLASS_NAME, "hays__job__details__your-qualifications")
            details = competences.find_elements(By.CSS_SELECTOR, "li")
            competences_array = []
            for i in details:
                competences_array.append(i.text)

            advantages =  browser.find_element(By.CLASS_NAME, "hays__job__details__your-advantages")
            details = advantages.find_elements(By.CSS_SELECTOR, "li")
            advantages_array = []
            for i in details:
                advantages_array.append(i.text)

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
        except Exception as err:
            mylogger.warning(f"Unexpected ERROR Taking Info {err}")

    return propositions

def ReturnData(searchWord,oferts):
    file_data = dict({"Key": searchWord,
    "quantity": len(oferts),
        "data":[]})
    file_data["data"] = oferts
    return file_data