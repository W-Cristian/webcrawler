import sys
sys.path.append('/app/utilities')
from logger import mylogger
from selenium.webdriver.common.by import By
import time
from .general_resources import Generate_browser

def RedirectPage(searchWord):
    url = f"https://www.michaelpage.de/jobs/{searchWord}?sort_by=most_recent"
    browser = Generate_browser()
    time.sleep(2)
    browser.get(url)
    time.sleep(2)

    return browser

def Make_list (browser):
    divBox = browser.find_elements(By.XPATH, "//li[@class='views-row']")
    index = range(0, len(divBox))
    propositions = []
    
    for i in index:
    
        link = divBox[i].find_element(By.CSS_SELECTOR, "a")
        obj = {
        "header" : link.text,
        "link" : link.get_attribute('href')
        }    
        propositions.append(obj)
    mylogger.debug("taken -{}- links ...".format(len(propositions)))

    return propositions

def TakeInfo (browser,data,quantity=None):
    if quantity is not None:
        index = range(0,quantity)
    else:
        index = range(0, len(data))
    
    count = 0
    propositions = []
    for x in index:

        count=count+1
        mylogger.debug("taking details from -{}- link: {}".format(count,data[x]["link"]))

        try:
            browser.get(data[x]["link"])
            time.sleep(2)
            container =  browser.find_element(By.ID, "job-description")
            last_update = container.find_element(By.CSS_SELECTOR, "p").text

            tasks =  container.find_elements(By.XPATH, ".//div[@class='job_advert__job-desc-role']//li")
            task_array = ""
            for i in tasks:
                task_array = task_array + i.text + "|"

            competences = container.find_elements(By.XPATH, ".//div[@class='job_advert__job-desc-candidate']//li")
            competences_array = ""
            for i in competences:
                competences_array = competences_array + i.text + "|"

            contact_holder = container.find_elements(By.XPATH, ".//div[@class='job-contact-info']//div[@class='field--item']")
            contact = {"reference_number" : contact_holder[1].text,
                    "name" : contact_holder[0].text,
                    "telephone" : contact_holder[2].text
                    }

            details = browser.find_elements(By.XPATH, "//div[@id='summary']//dd[@class='field--item summary-detail-field-value']")
            labels_details = browser.find_elements(By.XPATH, "//div[@id='summary']//dt[@class='field--label summary-detail-field-label']")

            detailsobj = {}
            index = range(0, len(details))
            for i in index:
                detailsobj[labels_details[i].text] = details[i].text

            obj = {
            "header" : data[x]["header"],
            "prospectnumber" : contact_holder[1].text,
            "tasks" : task_array[:-1],
            "competences" : competences_array[:-1],
            "details" : detailsobj,
            "contact" : contact,
            "link" : data[x]["link"]
            }     
            propositions.append(obj)

        except Exception as err:
            mylogger.warning(f"Unexpected ERROR Taking Info {err}")
    return propositions