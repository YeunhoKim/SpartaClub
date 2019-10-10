from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient as mg

app = Flask(__name__)
client = mg('localhost', 27017)
db = client.orders

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/order', methods=['POST'])
def order_saving():
    name = request.form['name_give']
    count = request.form['count_give']
    address = request.form['address_give']
    phone = request.form['phone_give']
    item = request.form['item_give']
    order = {'name' : name,
             'count' : count,
             'address' : address,
             'phone' : phone,
             'item':item}
    db.orders.insert_one(order)
    return jsonify({'result': 'success'})

@app.route('/order', methods=['GET'])
def listing():
    item_receive = request.args.get('item_give')
    result = list(db.orders.find({'item':item_receive},{'_id':0}))
    return jsonify({'result': 'success', 'orders':result})

if __name__ == '__main__':
    app.run('127.0.0.1', port=5000, debug=True)
