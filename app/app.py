from flask import Flask, jsonify, request
import freelancer_base
import hays_Base
app = Flask(__name__)

@app.route('/ping')
def ping():
    return jsonify({'message':'pong'})
    
@app.route('/')
def status():
    return 'Alive'

@app.route('/freelancer/<string:keyword>')
def respose(keyword):

    browser = freelancer_base.RedirectPage(keyword)
    oferts = freelancer_base.TakeInfo(browser)
    data = freelancer_base.ReturnData(keyword,oferts)
    freelancer_base.Logout(browser)
    return jsonify({'message':data})


@app.route('/freelancer', methods =["POST"])
def request_freelancer():
    user = request.json["user"]
    searchWord = request.json["key"]
    password = request.json["pass"]
    quantity=None
    if "quantity" in request.json:
        quantity=int(request.json['quantity'])

    data = freelancer_base.Take_Detail_data(user, password, searchWord,quantity)
    quantity_return = len(data)
    return jsonify({'user':user,
        'keyword':searchWord,
        'quantity':quantity_return,
        'data':data})
    
@app.route('/hays/<string:keyword>')
def request_hays(keyword):
    browser = hays_Base.RedirectPage(keyword)
    oferts = hays_Base.Make_list(browser)
    data = hays_Base.TakeInfo(browser,oferts)
    quantity_return = len(data)
    browser.quit()

    return jsonify({'keyword' : keyword,
        'quantity' : quantity_return,
        'data':data})

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True, port=4000)