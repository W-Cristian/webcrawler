import sys
sys.path.append('/app/utilities')
from logger import mylogger
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def Redirect_page(searchWord,browser):
    url = f"https://www.gulp.de/gulp2/g/projekte?query={searchWord}&order=DATE_DESC"
    mylogger.info(f"searchword -----{searchWord}")
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
            EC.presence_of_element_located((By.XPATH, "//ul[@class='ng-star-inserted']"))
            )
    except Exception as e:
        mylogger.error(e)
        raise e

    divBox = browser.find_elements(By.XPATH, "//ul[@class='ng-star-inserted']//li")
    index = range(0, len(divBox))
    propositions = []
    
    for i in index:
        link = divBox[i].find_element(By.CSS_SELECTOR, "a")
        firma = None
        try:
            firma = divBox[i].find_element(By.XPATH, ".//span[@class='company ng-star-inserted']").text
        except Exception as e:
            mylogger.info("EXPECTED ERROR: NOT FOUND  - span[@class='company ng-star-inserted']")
            
        obj = {
        "header" : link.get_attribute('text'),
        "link" : link.get_attribute('href'),
        "firma" : firma
        }    
        
        propositions.append(obj)
    mylogger.info("taken -{}- links ...".format(len(propositions)))
    return propositions

def Take_info (browser,data,quantity=None):
    index = range(0, len(data))
    
    propositions = {"gulp" : [],
                   "solcom" : []}
    for x in index:
        if "agentur" in data[x]["link"]:
            mylogger.info("taking details from link: {}".format(data[x]["link"]))
            try:
                browser.get(data[x]["link"])
                element = WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "element-box"))
                    )
            except Exception as e:
                mylogger.error(e)
                raise e
            container =  browser.find_element(By.CLASS_NAME, "element-box")
            description_container = container.find_elements(By.CLASS_NAME, "form-value")
            detailsobj = {
            "Referenznummer" : description_container[0].text,
            "Veröffentlicht" : description_container[1].text,
            "Beginn" : description_container[2].text,
            "Dauer" : description_container[3].text,
            "Einsatzort" : description_container[4].text,
            }
            description_array = description_container[5].text,

            competences_array = description_container[6].find_elements(By.XPATH, ".//div")
            competences = ""
            if len(competences_array) > 0: 
                for i in competences_array:
                    competences = competences + i.text + "|"
                competences = competences[:-1]
            else:
                competences = description_container[6].text
                
            contact_array = container.find_elements(By.XPATH, ".//section[@class='ng-star-inserted']//div[@class='ng-star-inserted']")
            link = container.find_element(By.XPATH, ".//a[@class='encrypted-mail']")
            mail = link.get_attribute('data-pre')+"@"+link.get_attribute('data-post')
            contact = {
            "name" : contact_array[0].text,
            "telephon" : None,
            "mail" : mail,
            "firma" : contact_array[-2].text,
            "adresse" : contact_array[-1].text
            }

            if len(contact_array) > 5:
                contact["telephon"] = contact_array[1].text.strip("Tel.:")

            obj = {
            "header" : data[x]["header"],
            "contact" : contact,
            "description" : description_array[0],
            "prospectnumber" : detailsobj["Referenznummer"],
            "competences" : competences,
            "details" : detailsobj,
            "link" : data[x]["link"]
            }     
            
            propositions["gulp"].append(obj)

        if data[x]["firma"] != None and "SOLCOM" in data[x]["firma"].upper():
            mylogger.info("taking details from link: {}".format(data[x]["link"]))
            browser.get(data[x]["link"])
            time.sleep(2)

            link = browser.find_element(By.PARTIAL_LINK_TEXT, 'wechseln').get_attribute('href')
            obj = {
            "header" : data[x]["header"],
            "link" : link,
            "firma" : data[x]["firma"]
            }
            propositions["solcom"].append(obj)

    return propositions

def TakeInfo_solcom (browser,solcom_data):

    index = range(0, len(solcom_data))
    
    propositions_solcom = []
    for x in index:
        mylogger.info(F"taking details from solcom link: {solcom_data[x]['link']}")
        browser.get(solcom_data[x]["link"])
        try:
            element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "infos"))
                )
        except Exception as e:
            mylogger.error(e)
            raise e

        container =  browser.find_element(By.CLASS_NAME, "infos")
        container_array = container.find_elements(By.CSS_SELECTOR, "div")
        text = ""
        for i in container_array:
            text = text + i.text +"\n"
        text_array = text.replace("\n",":").split(":")

        detailsobj = {
            text_array[0] : text_array[1],#Starttermin
            text_array[3] : text_array[4],#Stellentyp
            text_array[5] : text_array[6],#Einsatzort
            text_array[8] : text_array[9]#Dauer
        }

        description = browser.find_element(By.XPATH, ".//section[@class='section2 text section details cf']").text
        obj = {
        "header" : solcom_data[x]["header"],
        "description" : description,
        "prospectnumber" : text_array[12],
        "details" : detailsobj,
        "link" : solcom_data[x]["link"]
        }     
        propositions_solcom.append(obj)

    return propositions_solcom