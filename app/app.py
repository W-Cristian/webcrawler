from flask import Flask, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint
import freelance_base
import hays_Base
import michaelpage_Base
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

    browser = freelance_base.RedirectPage(keyword)
    oferts = freelance_base.TakeInfo(browser)
    data = freelance_base.ReturnData(keyword,oferts)
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
    browser = hays_Base.RedirectPage(keyword)
    oferts = hays_Base.Make_list(browser)
    data = hays_Base.TakeInfo(browser,oferts)
    quantity_return = len(data)
    browser.quit()

    return jsonify({'keyword' : keyword,
        'quantity' : quantity_return,
        'data':data})

@app.route('/michaelpage/<string:keyword>')
def crawl_michaelpage(keyword):
    browser = michaelpage_Base.RedirectPage(keyword)
    oferts = michaelpage_Base.Make_list(browser)
    data = michaelpage_Base.TakeInfo(browser,oferts)
    quantity_return = len(data)
    browser.quit()

    return jsonify({'keyword' : keyword,
        'quantity' : quantity_return,
        'data':data})

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True, port=4000)