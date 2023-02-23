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
    respose_code = 500
    if "ACCESS_TOKEN" in request.headers:
        access_token = request.headers.get('ACCESS_TOKEN', type=str)
        if Verify_credentials(access_token):
            valid = True
        else:
            respose_code = 403
    else:
        respose_code = 403

    if "keyword" in request.json:
        if request.json["keyword"] != "":
            keyword = request.json["keyword"]
        else:
            respose_code = 400
    else:
        respose_code = 400

    if valid and keyword:
        url_keyword = Filter_keyword(keyword)
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

RESPOSE_CODE_MESSAGE = {403:"Forbidden - invalid ACCESS_TOKEN",
                        400:"Bad Request - Missing keyword",
                        460:"Bad Request - Missing user or password",
                        500:"Server Unknow Error"}

def Generate_error_message(RESPOSE_CODE, keyword, ACCESS_TOKEN):
    if RESPOSE_CODE > 459 and RESPOSE_CODE < 470:
        respose_code = 400
    else:
        respose_code = RESPOSE_CODE
    
    return (
                respose_code,
                {'keyword' : keyword,
                'ACCESS_TOKEN' : ACCESS_TOKEN,
                'status': RESPOSE_CODE_MESSAGE[RESPOSE_CODE] }
            )

def Filter_keyword(keyword):
    url_keyword = keyword
    url_keyword = url_keyword.replace("#","%23")
    url_keyword = url_keyword.replace("/","%2F")
    url_keyword = url_keyword.replace(" ","+")
    return url_keyword

# browser.save_screenshot('screenshot.png')
