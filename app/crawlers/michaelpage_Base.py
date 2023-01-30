import sys
sys.path.append('/app/utilities')
from logger import mylogger
from selenium.webdriver.common.by import By
import time

def Redirect_page(searchWord,browser):
    # This page treats the transformation of special characters differently,
    # so it is done directly in the text passed by parameter.
    searchWord = searchWord.replace('#','').replace('/','-').replace(' ','-').replace('.','').lower()
    url = f"https://www.michaelpage.de/jobs/{searchWord}?sort_by=most_recent"
    mylogger.info(f"searchword -----{searchWord}")
    browser.get(url)
    time.sleep(3)

    return browser

def Make_list (browser):
    divBox = browser.find_elements(By.XPATH, "//li[@class='views-row']")
    index = range(0, len(divBox))
    propositions = []

    # body = browser.find_element(By.CSS_SELECTOR, "body").get_attribute("innerHTML")
    # lista = browser.find_elements(By.CLASS_NAME, "views-row")

    # mylogger.info(f" lista -{len(lista)}- ")
    # f = open("michaelpage_Base.html", "a")
    # f.write(body)
    # f.close()
    for i in index:
    
        link = divBox[i].find_element(By.CSS_SELECTOR, "a")
        obj = {
        "header" : link.text,
        "link" : link.get_attribute('href')
        }
        propositions.append(obj)
    mylogger.info("taken -{}- links ...".format(len(propositions)))

    return propositions

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

        header =  browser.find_element(By.CLASS_NAME, "job-title").text
        try:
            container =  browser.find_element(By.ID, "job-description")
        except Exception as err:
            mylogger.info(f"EXPETED ERROR - NOT FOUND ------job-description IN -{data[x]['link']}- SKIP")
            continue

        last_update = container.find_element(By.CSS_SELECTOR, "p").text

        tasks_container =  container.find_element(By.XPATH, ".//div[@class='job_advert__job-desc-role']")
        task_array = ""
        tasks = tasks_container.find_elements(By.CSS_SELECTOR, "li")
        if len(tasks) > 0:
            for i in tasks:
                task_array = task_array + i.text + "|"
                task_array = task_array[:-1]
        else:
            task_array = tasks_container.text
        

        competences_container = container.find_element(By.XPATH, ".//div[@class='job_advert__job-desc-candidate']")
        competences_array = ""
        competences = competences_container.find_elements(By.CSS_SELECTOR, "li")
        if len(competences) > 0:
            for i in competences:
                competences_array = competences_array + i.text + "|"
                competences_array = competences_array[:-1]
        else:
            competences_array = competences_container.text

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
        "header" : header,
        "prospectnumber" : contact_holder[1].text,
        "tasks" : task_array,
        "competences" : competences_array,
        "details" : detailsobj,
        "contact" : contact,
        "link" : data[x]["link"]
        }     
        propositions.append(obj)

    return propositions