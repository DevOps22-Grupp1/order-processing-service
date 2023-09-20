from flask import Flask, jsonify, request, json
from prometheus_flask_exporter import PrometheusMetrics
from pymongo import MongoClient
import os

db_username = os.environ.get("DB_USERNAME")
db_password = os.environ.get("DB_PASSWORD")
app = Flask(__name__)
metrics = PrometheusMetrics(app)
client = MongoClient('mongo', 27017, username=db_username,
                     password=db_password)
db_port = os.environ.get("DB_PORT")

db = client.allOrders
query = db.orders



@app.route('/')
def hello_world():
    return 'Hello, this is Order processing catalog service'

@app.route('/api/orders', methods=['GET'])
def get_all_orders():
    data = []
    orders = db.orders.find()
    for order in orders:
        order['_id'] = str(order['_id'])
        data.append(order)
    return jsonify(data)

@app.route('/api/order/<order_id>', methods=['GET'])
def get_single_order(order_id):
    data = []
    order = db.orders.find_one({"id": int(order_id)})
    if order:
        order['_id'] = str(order['_id'])
        data.append(order)
    return jsonify(data)

@app.route('/api/order', methods=['POST'])
def post_order():
    data = json.loads(request.data)
    data["id"] = increment_order()
    db.orders.insert_one(data)
    return f"A new order has been added"

@app.route('/api/order/<order_id>', methods=['DELETE'])
def delete_order(order_id):
    db.orders.delete_one({"id": int(order_id)})
    return f"Deleted the order from the database"

@app.route('/api/order/<order_id>', methods=['PUT'])
def update_order(order_id):
    data = json.loads(request.data)
    data["id"] = int(order_id)
    db.orders.find_one_and_update({'id' : int(order_id)}, {'$set': data})
    return f"Updated the order in the database"

def increment_order():
    return str(db.orders.count_documents({}))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=db_port, debug=False)