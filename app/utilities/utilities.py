import os
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')

def Verify_credentials(TOKEN):
    return TOKEN==ACCESS_TOKEN

def Handler_request(request):
    valid = False
    keyword = None
    url_keyword = None
    quantity=None
    access_token = None
    respose_code = 290
    if "ACCESS_TOKEN" in request.headers:
        access_token = request.headers.get('ACCESS_TOKEN', type=str)
    else:
        respose_code = 210

    if "keyword" in request.json:
        keyword = request.json["keyword"]
    else:
        respose_code = 211

    if access_token and keyword:
        url_keyword = Filter_keyword(keyword)
        valid = Verify_credentials(access_token)
        quantity=None
        if "MaxQuantity" in request.json:
            quantity=int(request.json['MaxQuantity'])
    else:
        valid = False

    return {"valid" : valid,
    "quantity" : quantity,
    "raw_keyword" : keyword,
    "url_keyword" : url_keyword,
    "access_token" : access_token,
    "respose_code" : respose_code
    }

RESPOSE_CODE_MESSAGE = {210:"ERROR invalid ACCESS_TOKEN",
                        211:"ERROR Missing keyword",
                        213:"ERROR Missing user or password",
                        290:"Unknow error"}

def Filter_keyword(keyword):
    url_keyword = keyword
    url_keyword = url_keyword.replace("#","%23")
    url_keyword = url_keyword.replace("/","%2F")
    url_keyword = url_keyword.replace(" ","+")
    return url_keyword