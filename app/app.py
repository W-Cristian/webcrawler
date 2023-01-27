from flask import Flask, jsonify, request, make_response
from flask_swagger_ui import get_swaggerui_blueprint
from  utilities.utilities import Verify_credentials,Handler_request,RESPOSE_CODE_MESSAGE
from  utilities.logger import mylogger

import crawlers.freelance_base as freelance_base
import crawlers.hays_Base as hays_Base
import crawlers.michaelpage_Base as michaelpage_Base
import crawlers.solcom_base as solcom_base
import crawlers.gulp_base as gulp_base
import crawlers.ferchau_base as ferchau_base
import crawlers.austinfraser_base as austinfraser_base
from crawlers.general_resources import Generate_browser

app = Flask(__name__)

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/swagger.json'  # Our API url (can of course be a local resource)

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "CODUCT Crawlers"
    },
)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static',path)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/')
def status():
    return "Alive"

@app.route('/api/freelance', methods =["POST"])
def Crawl_post_freelance():
    handler = Handler_request(request)
    user=None
    password = None
    if "user" in request.json and "pass" in request.json:
        user = request.json["user"]
        password = request.json["pass"]
    else:
        handler["respose_code"] = 213

    if handler["valid"] and user and password:
        browser = Generate_browser()
        keyword = handler["raw_keyword"]
        url_keyword = handler["url_keyword"]
        quantity = handler["quantity"]
        access_token = handler["access_token"]    

        try:
            log_browser = freelance_base.LogIn(user, password,browser)
            data = freelance_base.Take_detail_data(log_browser, url_keyword,quantity)
            quantity_return = len(data)
            return jsonify({'user':user,
                'keyword':keyword,
                'quantity':quantity_return,
                'data':data})
        except Exception as err:
            mylogger.warning(f"Unexpected ERROR Taking Info {err}")
            raise err
        finally:
            browser.quit()
            mylogger.debug(f"Closing Browser")

    else:
        error_code = handler["respose_code"]
        error_m = RESPOSE_CODE_MESSAGE[error_code]
        invalid_ACCESS_TOKEN = jsonify({'keyword' : handler["raw_keyword"],
                'ACCESS_TOKEN' : handler["access_token"],
                'status': error_m })
        resp = make_response(invalid_ACCESS_TOKEN, error_code)
        return resp
    
@app.route('/api/hays/', methods =["POST"])
def rcrawl_hays():
    handler = Handler_request(request)
    if handler["valid"]:
        browser = Generate_browser()
        keyword = handler["raw_keyword"]
        url_keyword = handler["url_keyword"]
        quantity = handler["quantity"]
        access_token = handler["access_token"]
        try:
            browser = hays_Base.Redirect_page(keyword,browser)
            oferts = hays_Base.Make_list(browser)
            data = hays_Base.Take_info(browser,oferts,quantity)
            quantity_return = len(data)
            return jsonify({'keyword' : keyword,
                'quantity' : quantity_return,
                'data':data})
        except Exception as err:
            mylogger.warning(f"Unexpected ERROR Taking Info {err}")
            raise err
        finally:
            browser.quit()
            mylogger.debug(f"Closing Browser")

    else:
        error_code = handler["respose_code"]
        error_m = RESPOSE_CODE_MESSAGE[error_code]
        invalid_ACCESS_TOKEN = jsonify({'keyword' : handler["raw_keyword"],
                'ACCESS_TOKEN' : handler["access_token"],
                'status': error_m })
        resp = make_response(invalid_ACCESS_TOKEN, error_code)
        return resp

@app.route('/api/michaelpage/', methods =["POST"])
def crawl_michaelpage():
    handler = Handler_request(request)
    if handler["valid"]:
        browser = Generate_browser()
        keyword = handler["raw_keyword"]
        url_keyword = handler["url_keyword"]
        quantity = handler["quantity"]
        access_token = handler["access_token"]
        try:
            browser = michaelpage_Base.Redirect_page(keyword,browser)
            oferts = michaelpage_Base.Make_list(browser)
            data = michaelpage_Base.Take_info(browser,oferts,quantity)
            quantity_return = len(data)
            return jsonify({'keyword' : keyword,
                'quantity' : quantity_return,
                'data':data})
        except Exception as err:
            mylogger.warning(f"Unexpected ERROR Taking Info {err}")
            raise err
        finally:
            browser.quit()
            mylogger.debug(f"Closing Browser")

    else:
        error_code = handler["respose_code"]
        error_m = RESPOSE_CODE_MESSAGE[error_code]
        invalid_ACCESS_TOKEN = jsonify({'keyword' : handler["raw_keyword"],
                'ACCESS_TOKEN' : handler["access_token"],
                'status': error_m })
        resp = make_response(invalid_ACCESS_TOKEN, error_code)
        return resp

@app.route('/api/solcom/', methods =["POST"])
def crawl_solcom():
    handler = Handler_request(request)
    if handler["valid"]:
        browser = Generate_browser()
        keyword = handler["raw_keyword"]
        url_keyword = handler["url_keyword"]
        quantity = handler["quantity"]
        access_token = handler["access_token"]
        try:
            browser = solcom_base.Redirect_page(url_keyword,browser)
            oferts = solcom_base.Make_list(browser)
            data = solcom_base.Take_info(browser,oferts,quantity)
            quantity_return = len(data)
            return jsonify({'keyword' : keyword,
                'quantity' : quantity_return,
                'data':data})

        except Exception as err:
            mylogger.warning(f"Unexpected ERROR Taking Info {err}")
            raise err
        finally:
            browser.quit()
            mylogger.debug(f"Closing Browser")

    else:
        error_code = handler["respose_code"]
        error_m = RESPOSE_CODE_MESSAGE[error_code]
        invalid_ACCESS_TOKEN = jsonify({'keyword' : handler["raw_keyword"],
                'ACCESS_TOKEN' : handler["access_token"],
                'status': error_m })
        resp = make_response(invalid_ACCESS_TOKEN, error_code)
        return resp

@app.route('/api/gulp/', methods =["POST"])
def crawl_gulp():
    args = request.args
    exclusive_gulp = args.get("exclusive_gulp", type=bool)
    handler = Handler_request(request)
    if handler["valid"]:
        browser = Generate_browser()
        keyword = handler["raw_keyword"]
        url_keyword = handler["url_keyword"]
        quantity = handler["quantity"]
        access_token = handler["access_token"]
        try:
            browser = gulp_base.Redirect_page(keyword,browser)
            oferts = gulp_base.Make_list(browser)
            data = gulp_base.Take_info(browser,oferts)
            if not exclusive_gulp:
                propositions_solcom = gulp_base.TakeInfo_solcom(browser,data["solcom"])
                data["solcom"] = propositions_solcom
            else:
                data["solcom"] = None

            return jsonify({'keyword' : keyword,
                'data':data})
        except Exception as err:
            mylogger.warning(f"Unexpected ERROR Taking Info {err}")
            raise err
        finally:
            browser.quit()
            mylogger.debug(f"Closing Browser")

    else:
        error_code = handler["respose_code"]
        error_m = RESPOSE_CODE_MESSAGE[error_code]
        invalid_ACCESS_TOKEN = jsonify({'keyword' : handler["raw_keyword"],
                'ACCESS_TOKEN' : handler["access_token"],
                'status': error_m })
        resp = make_response(invalid_ACCESS_TOKEN, error_code)
        return resp

@app.route('/api/ferchau/', methods =["POST"])
def crawl_ferchau():
    quantity = 20
    handler = Handler_request(request)
    if handler["valid"]:
        browser = Generate_browser()
        keyword = handler["raw_keyword"]
        url_keyword = handler["url_keyword"]
        if handler["quantity"]:
            quantity = handler["quantity"]
        access_token = handler["access_token"]
        try:
            oferts = ferchau_base.Get_proposals(keyword,quantity)
            data = ferchau_base.Take_data(oferts)
            quantity_return = len(data)
            return jsonify({'keyword' : keyword,
                'quantity' : quantity_return,
                'data':data})

        except Exception as err:
            mylogger.warning(f"Unexpected ERROR Taking Info {err}")
            raise err
        finally:
            browser.quit()
            mylogger.debug(f"Closing Browser")

    else:
        error_code = handler["respose_code"]
        error_m = RESPOSE_CODE_MESSAGE[error_code]
        invalid_ACCESS_TOKEN = jsonify({'keyword' : handler["raw_keyword"],
                'ACCESS_TOKEN' : handler["access_token"],
                'status': error_m })
        resp = make_response(invalid_ACCESS_TOKEN, error_code)
        return resp

@app.route('/api/austinfraser/', methods =["POST"])
def crawl_austinfraser():
    handler = Handler_request(request)
    if handler["valid"]:
        browser = Generate_browser()
        keyword = handler["raw_keyword"]
        url_keyword = handler["url_keyword"]
        quantity = handler["quantity"]
        access_token = handler["access_token"]
        try:
            browser = austinfraser_base.Redirect_page(url_keyword,browser)
            oferts = austinfraser_base.Make_list(browser)
            data = austinfraser_base.Take_info(browser,oferts,quantity)
            quantity_return = len(data)
            return jsonify({'keyword' : keyword,
                'quantity' : quantity_return,
                'data':data})

        except Exception as err:
            mylogger.warning(f"Unexpected ERROR Taking Info {err}")
            raise err
        finally:
            browser.quit()
            mylogger.debug(f"Closing Browser")

    else:
        error_code = handler["respose_code"]
        error_m = RESPOSE_CODE_MESSAGE[error_code]
        invalid_ACCESS_TOKEN = jsonify({'keyword' : handler["raw_keyword"],
                'ACCESS_TOKEN' : handler["access_token"],
                'status': error_m })
        resp = make_response(invalid_ACCESS_TOKEN, error_code)
        return resp

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True, port=4000)