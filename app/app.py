from flask import Flask, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint
import freelance_base
import hays_Base
import michaelpage_Base
import solcom_base
import gulp_base

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

# @app.route('/ping')
# def ping():
#     return jsonify({'message':'pong'})
    
@app.route('/')
def status():
    return 'Alive'

@app.route('/freelance/<string:keyword>')
def respose(keyword):
    args = request.args
    quantity = args.get("MaxQuantity", type=int)
    browser = freelance_base.RedirectPage(keyword)
    oferts = freelance_base.TakeInfo(browser)
    data = freelance_base.ReturnData(keyword,oferts,quantity)
    freelance_base.Logout(browser)
    return jsonify({'message':data})


@app.route('/freelance', methods =["POST"])
def crawl_freelancer():
    user = request.json["user"]
    searchWord = request.json["key"]
    password = request.json["pass"]
    quantity=None
    if "quantity" in request.json:
        quantity=int(request.json['quantity'])

    data = freelance_base.Take_Detail_data(user, password, searchWord,quantity)
    quantity_return = len(data)
    return jsonify({'user':user,
        'keyword':searchWord,
        'quantity':quantity_return,
        'data':data})
    
@app.route('/hays/<string:keyword>')
def rcrawl_hays(keyword):
    args = request.args
    quantity = args.get("MaxQuantity", type=int)
    browser = hays_Base.RedirectPage(keyword)
    oferts = hays_Base.Make_list(browser)
    data = hays_Base.TakeInfo(browser,oferts,quantity)
    quantity_return = len(data)
    browser.quit()

    return jsonify({'keyword' : keyword,
        'quantity' : quantity_return,
        'data':data})

@app.route('/michaelpage/<string:keyword>')
def crawl_michaelpage(keyword):
    args = request.args
    quantity = args.get("MaxQuantity", type=int)
    browser = michaelpage_Base.RedirectPage(keyword)
    oferts = michaelpage_Base.Make_list(browser)
    data = michaelpage_Base.TakeInfo(browser,oferts,quantity)
    quantity_return = len(data)
    browser.quit()

    return jsonify({'keyword' : keyword,
        'quantity' : quantity_return,
        'data':data})

@app.route('/solcom/<string:keyword>')
def crawl_solcom(keyword):
    args = request.args
    quantity = args.get("MaxQuantity", type=int)
    browser = solcom_base.RedirectPage(keyword)
    oferts = solcom_base.Make_list(browser)
    data = solcom_base.TakeInfo(browser,oferts,quantity)
    quantity_return = len(data)
    browser.quit()

    return jsonify({'keyword' : keyword,
        'quantity' : quantity_return,
        'data':data})

@app.route('/gulp/<string:keyword>')
def crawl_gulp(keyword):
    args = request.args
    exclusive_gulp = args.get("exclusive_gulp", type=bool)
    browser = gulp_base.RedirectPage(keyword)
    oferts = gulp_base.Make_list(browser)
    data = gulp_base.TakeInfo(browser,oferts)
    if not exclusive_gulp:
        propositions_solcom = gulp_base.TakeInfo_solcom(browser,data["solcom"])
        data["solcom"] = propositions_solcom
    else:
        data["solcom"] = None
    browser.quit()
    
    return jsonify({'keyword' : keyword,
        'data':data})

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True, port=4000)