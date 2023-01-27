import sys
sys.path.append('/app/utilities')
from logger import mylogger
import requests
import json

def Get_proposals(searchWord,quantity):
    url = f'https://api.ferchau.com/v4/recruiting/search?count=ferchau&limit={quantity}&query={searchWord}'
    respose = requests.request('GET',url, data="",headers={})
    mylogger.debug(f"searchword -----{searchWord}")
    return json.loads(respose.text)

def Take_details (id):
    url = f'https://api.ferchau.com/v4/recruiting/details/{id}'
    respose = requests.request('GET',url, data="",headers={})
    ofert = json.loads(respose.text)
    contactobj = {
        "name" : ofert["sanspkomplett"],
        "adresse" : ofert["sstrasse"] + " " + ofert["splz"] + " " + ofert["sort"],
        "telephone" :  ofert["sfon"],
        "mail" :  ofert["sanspemail"],
    }
    detailsobj = {
        "firma" : ofert["sorganisationbez"],
        "starttermin" : ofert["seintritt"],
        "einsatzort" :  ofert["seinsatzort"],
    }
    url = f"https://www.ferchau.com/de/en/applicants/jobs/{ofert['njobid']}"
    obj = {
    "header" : ofert["sjobbez"],
    "description" : ofert["seinleitung"],
    "prospectnumber" : ofert["sjobnr"],
    "tasks" : ofert["saufgabe"],
    "competences" : ofert["svoraussetzung"],
    "details" : detailsobj,
    "contact" : contactobj,
    "link" : url
    }
    return obj


def Take_data(oferts):
    propositions = []
    for i in oferts['matches']:
        id = i['njobid']
        respose_obj = Take_details(id)
        propositions.append(respose_obj)
    return propositions