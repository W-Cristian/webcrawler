from flask import Flask, jsonify, request, make_response
from flask_swagger_ui import get_swaggerui_blueprint
from  utilities.utilities import Verify_credentials
from  utilities.logger import mylogger

import crawlers.freelance_base as freelance_base
import crawlers.hays_Base as hays_Base
import crawlers.michaelpage_Base as michaelpage_Base
import crawlers.solcom_base as solcom_base
import crawlers.gulp_base as gulp_base
import crawlers.ferchau_base as ferchau_base
from crawlers.general_resources import Generate_browser

app = Flask(__name__)

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/swagger.json'  # Our API url (can of course be a local resource)

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Test application"
    },
)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static',path)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/')
def status():
    return "Alive"

@app.route('/freelance/<string:keyword>')
def respose(keyword):
    args = request.args
    quantity = args.get("MaxQuantity", type=int)
    access_token = args.get("ACCESS_TOKEN", type=str)
    if Verify_credentials(access_token):
        browser = Generate_browser()
        try:
            browser = freelance_base.RedirectPage(keyword,browser)
            oferts = freelance_base.TakeInfo(browser,quantity)
            freelance_base.Logout(browser)
            return jsonify({'keyword' : keyword,
                'quantity' : len(oferts),
                'data':oferts})
        except Exception as err:
            mylogger.warning(f"Unexpected ERROR Taking Info {err}")
            raise err
        finally:
            browser.quit()
            mylogger.debug(f"Closing Browser")

    else:
        invalid_ACCESS_TOKEN = jsonify({'keyword' : keyword,
                'ACCESS_TOKEN' : access_token,
                'status':'ERROR invalid ACCESS_TOKEN'})
        resp = make_response(invalid_ACCESS_TOKEN, 210)
        return resp


@app.route('/freelance', methods =["POST"])
def crawl_freelancer():
    user = request.json["user"]
    searchWord = request.json["key"]
    password = request.json["pass"]
    quantity=None
    if "quantity" in request.json:
        quantity=int(request.json['quantity'])
    access_token = request.json["ACCESS_TOKEN"]
    if Verify_credentials(access_token):
        browser = Generate_browser()
        try:
            log_browser = freelance_base.LogIn(user, password,browser)
            data = freelance_base.Take_Detail_data(log_browser, searchWord,quantity)
            quantity_return = len(data)
            return jsonify({'user':user,
                'keyword':searchWord,
                'quantity':quantity_return,
                'data':data})
        except Exception as err:
            mylogger.warning(f"Unexpected ERROR Taking Info {err}")
            raise err
        finally:
            browser.quit()
            mylogger.debug(f"Closing Browser")

    else:
        invalid_ACCESS_TOKEN = jsonify({'keyword' : keyword,
                'ACCESS_TOKEN' : access_token,
                'status':'ERROR invalid ACCESS_TOKEN'})
        resp = make_response(invalid_ACCESS_TOKEN, 210)
        return resp
    
@app.route('/hays/<string:keyword>')
def rcrawl_hays(keyword):
    args = request.args
    quantity = args.get("MaxQuantity", type=int)
    access_token = args.get("ACCESS_TOKEN", type=str)
    if Verify_credentials(access_token):
        browser = Generate_browser()
        try:
            browser = hays_Base.RedirectPage(keyword,browser)
            oferts = hays_Base.Make_list(browser)
            data = hays_Base.TakeInfo(browser,oferts,quantity)
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
        invalid_ACCESS_TOKEN = jsonify({'keyword' : keyword,
                'ACCESS_TOKEN' : access_token,
                'status':'ERROR invalid ACCESS_TOKEN'})
        resp = make_response(invalid_ACCESS_TOKEN, 210)
        return resp

@app.route('/michaelpage/<string:keyword>')
def crawl_michaelpage(keyword):
    args = request.args
    quantity = args.get("MaxQuantity", type=int)
    access_token = args.get("ACCESS_TOKEN", type=str)
    if Verify_credentials(access_token):
        browser = Generate_browser()
        try:
            browser = michaelpage_Base.RedirectPage(keyword,browser)
            oferts = michaelpage_Base.Make_list(browser)
            data = michaelpage_Base.TakeInfo(browser,oferts,quantity)
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
        invalid_ACCESS_TOKEN = jsonify({'keyword' : keyword,
                'ACCESS_TOKEN' : access_token,
                'status':'ERROR invalid ACCESS_TOKEN'})
        resp = make_response(invalid_ACCESS_TOKEN, 210)
        return resp

@app.route('/solcom/<string:keyword>')
def crawl_solcom(keyword):
    args = request.args
    quantity = args.get("MaxQuantity", type=int)
    access_token = args.get("ACCESS_TOKEN", type=str)
    if Verify_credentials(access_token):
        browser = Generate_browser()
        try:
            browser = solcom_base.RedirectPage(keyword,browser)
            oferts = solcom_base.Make_list(browser)
            data = solcom_base.TakeInfo(browser,oferts,quantity)
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
        invalid_ACCESS_TOKEN = jsonify({'keyword' : keyword,
                'ACCESS_TOKEN' : access_token,
                'status':'ERROR invalid ACCESS_TOKEN'})
        resp = make_response(invalid_ACCESS_TOKEN, 210)
        return resp

@app.route('/gulp/<string:keyword>')
def crawl_gulp(keyword):
    args = request.args
    exclusive_gulp = args.get("exclusive_gulp", type=bool)
    access_token = args.get("ACCESS_TOKEN", type=str)
    if Verify_credentials(access_token):
        browser = Generate_browser()
        try:
            browser = gulp_base.RedirectPage(keyword,browser)
            oferts = gulp_base.Make_list(browser)
            data = gulp_base.TakeInfo(browser,oferts)
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
        invalid_ACCESS_TOKEN = jsonify({'keyword' : keyword,
                'ACCESS_TOKEN' : access_token,
                'status':'ERROR invalid ACCESS_TOKEN'})
        resp = make_response(invalid_ACCESS_TOKEN, 210)
        return resp


@app.route('/ferchau/<string:keyword>')
def crawl_ferchau(keyword):
    args = request.args
    quantity = args.get("MaxQuantity", type=int)
    access_token = args.get("ACCESS_TOKEN", type=str)
    if Verify_credentials(access_token):
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

    else:
        invalid_ACCESS_TOKEN = jsonify({'keyword' : keyword,
                'ACCESS_TOKEN' : access_token,
                'status':'ERROR invalid ACCESS_TOKEN'})
        resp = make_response(invalid_ACCESS_TOKEN, 210)
        return resp

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True, port=4000)