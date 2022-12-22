from flask import Flask, jsonify, request
from Freelancer_keyword import *
app = Flask(__name__)

@app.route('/ping')
def ping():
    return jsonify({'message':'pong'})
    
@app.route('/')
def status():
    return 'Alive'


@app.route('/freelancer/<string:keyword>')
def respose(keyword):

    browser = RedirectPage(keyword)
    oferts = TakeInfo (browser)
    data = ReturnData(keyword,oferts)
    return jsonify({'message':data})


@app.route('/freelancer', methods =["POST"])
def request_freelancer():
    print(request.json)
    user = request.json["user"]
    searchWord = request.json["key"]
    password = request.json["pass"]
    quantity=None
    print(quantity)
    if "quantity" in request.json:
        quantity=int(request.json['quantity'])
    data = Take_Detail_data(user, password, searchWord,quantity)
    return jsonify({'user':user,
        'keyword':searchWord,
        'quantity':len(data),
        'data':data})
    return quantity
    
if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True, port=4000)