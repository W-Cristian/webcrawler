from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from logger import mylogger

def RedirectPage(searchWord):
    url = "https://www.freelance.de/"
    browser = webdriver.Remote(command_executor='http://selenium:4444/wd/hub',
        desired_capabilities=DesiredCapabilities.FIREFOX)
    time.sleep(5)
    browser.get(url)
    time.sleep(2)

    search_el = browser.find_element(By.ID, 'search-text')
    search_el.send_keys(searchWord)
    time.sleep(2)

    submit_btn_el = browser.find_element(By.XPATH, "//button[@class='btn btn-primary'][@type='button']")
    submit_btn_el.click()
    time.sleep(2)
    browser.save_screenshot('screenshot.png')
    return browser

def TakeInfo (browser,quantity=None):
    divBox = browser.find_elements(By.XPATH, "//div[@class='list-item-main']")
    div_count = len(divBox)
    if quantity is not None:
        index = range(0,quantity)
        if len(index) > div_count:
            index = range(0, div_count)
    else:
        index = range(0, div_count)

    propositions = []
    for i in index:
        header = divBox[i].find_element(By.CSS_SELECTOR, "h3")
        link = header.find_element(By.CSS_SELECTOR, "a").get_attribute('href')
        firma = divBox[i].find_element(By.CLASS_NAME , 'company-name').text
        details = divBox[i].find_element(By.CLASS_NAME , 'icon-list')
        details_array = []
        detail = details.find_elements(By.CSS_SELECTOR, "li")
        detail
        for detail in details.find_elements(By.CSS_SELECTOR, "li"):
            details_array.append(detail.text)

        obj = {
        "header" : header.text,
        "firma" : firma,
        "details" : details_array,
        "link" : link
        }     
        mylogger.debug("-- links - {} ...".format(obj["link"]))
        propositions.append(obj)
    mylogger.debug("taken -{}- links ...".format(len(propositions)))
    return propositions

def ReturnData(searchWord,oferts,quantity=None):
    file_data = dict({"Key": searchWord,
    "quantity": len(oferts),
        "data":[]})
    file_data["data"] = oferts
    return file_data

def LogIn(user,password):

    url = "https://www.freelance.de/login.php"
    browser = webdriver.Remote('http://selenium:4444/wd/hub',
        desired_capabilities=DesiredCapabilities.FIREFOX)
    time.sleep(5)

    browser.get(url)
    time.sleep(2)

    user_el = browser.find_element(By.ID, 'username')
    user_el.send_keys(user)
    time.sleep(2)

    pass_el = browser.find_element(By.ID, 'password')
    pass_el.send_keys(password)
    time.sleep(2)

    submit_btn_el = browser.find_element(By.XPATH, "//input[@name='login'][@type='submit']")
    submit_btn_el.click()
    time.sleep(2)
    mylogger.debug("LogIn succesfully with credentials...")

    return browser

def Insert_search(log_browser,searchWord):
    project_url = f"https://www.freelance.de/search/project.php?__search_sort_by=2&__search_freetext={searchWord}&__search_sort_by_remote=2"
    log_browser.get(project_url)
    time.sleep(2)
    mylogger.debug("Looking for projects with -{}- as key ...".format(searchWord))

def Take_header(log_browser,url):
    log_browser.get(url)
    time.sleep(2)
    
    container = log_browser.find_element(By.XPATH, "//div[@class='panel project-detail online read']")
    title = container.find_element(By.XPATH,"//h1[@class='margin-bottom-xs']").text
    company_name = container.find_element(By.CSS_SELECTOR,"a").get_attribute('text')
    data = {'title':title,
           'company_name':company_name}
    
    list_detail = container.find_elements(By.CSS_SELECTOR,"li")
    for i in list_detail:
        if len(i.get_attribute('innerHTML').strip()) > 1:
            namelable = i.find_element(By.CSS_SELECTOR,"i").get_attribute('data-original-title')
            data[namelable] = i.text

    return data

def Take_project_description(log_browser):
    container = log_browser.find_element(By.XPATH, "//div[@class='panel-body highlight-text']")
    text = container.text.replace('\n', " ")
    return text

def Take_contact(log_browser):
    time.sleep(1)
    kontac_btns = log_browser.find_elements(By.CSS_SELECTOR, "button")
    mail = ""
    company = ""
    for i in kontac_btns:
        if i.text == 'Kontaktdaten anzeigen':
            kontac_btn = i
            panel = kontac_btn.find_element(By.XPATH,".//ancestor::div[@class='panel-body']")
            kontac_btn.click()
            time.sleep(3)

            links = panel.find_elements(By.CSS_SELECTOR,"a")
            company = links[0].get_attribute('text')
            for i in links:
                if "mailto:" in i.get_attribute('href'):
                    mail = i.get_attribute('href').replace('mailto:', "")
    
    infopanel = log_browser.find_element(By.XPATH,"//div[@id='contact_data']")
    sectors = infopanel.find_elements(By.CSS_SELECTOR,"div")
    count = 0
    reach_through = ""
    for i in sectors:
        if mail in i.text:
            reach_through = i.text.replace('\n', " ").strip()
        count = count+1
    lenght = len(sectors)-1
    
    adresse = sectors[lenght-1].text.replace('\n', " ")

    return {'company':company,
            'mail':mail,
            'reach_through':reach_through,
            'adresse':adresse
           }

def Logout(log_browser):
    url = "https://www.freelance.de/logout.php"
    log_browser.get(url)
    time.sleep(1)
    mylogger.debug("logout and close Browser...")

    log_browser.quit()

def Take_Detail_data(user, password, searchWord,quantity=None):
    log_browser = LogIn(user, password)
    Insert_search(log_browser,searchWord)
    list_url = TakeInfo (log_browser,quantity)
    detaildata = []
    count = 1
    for i in list_url:
        header = Take_header(log_browser,i["link"])
        description = Take_project_description(log_browser)
        try:
            contact = Take_contact(log_browser)
        except Exception as err:
            mylogger.warning(f"Unexpected ERROR Taking contact {err}")
            contact=None
        mylogger.debug("save data from -{}- link ...".format(count))

        count=count+1
        obj ={'url':i["link"]}
        obj['header'] = header
        obj['contact'] = contact
        obj['description'] = description
        detaildata.append(obj)
    Logout(log_browser)
    return detaildata