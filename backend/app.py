from flask import Flask, jsonify, request, json
from prometheus_flask_exporter import PrometheusMetrics
import pymongo
from pymongo import MongoClient

app = Flask(__name__)
metrics = PrometheusMetrics(app)

client = MongoClient('mongo-3', 27017, username='root', password='example')

db = client.allOrders
query = db.orders

@app.route('/')
def hello_world():
    return "Success", 200, {"Access-Control-Allow-Origin": "*"}


@app.route('/api/orders', methods=['GET'])
def get_all_orders():
    data = []
    todos = query.find()
    for doc in todos:
        doc['_id'] = str(doc['_id'])  # This does the trick! to what sais everyone else. 
        data.append(doc)
    return jsonify(data)


@app.route('/api/order/<order_id>', methods=['GET'])
def get_single_order(order_id):
    data = []
    todos = query.find({"id": int(order_id)})
    for doc in todos:
        doc['_id'] = str(doc['_id'])  # This does the trick!
        data.append(doc)
    return jsonify(data)


@app.route('/api/order', methods=['POST'])
def post_orders():
    data = json.loads(request.data)
    data["id"] = increment_post()
    query.insert_one(data)
    return f"a new post has been added"


@app.route('/api/order/<order_id>', methods=['DELETE'])
def delete_orders(order_id):
    query.delete_one({"id": int(order_id)})
    return f"delete the post from the database"

@app.route('/api/order/<order_id>', methods=['PUT'])
def update_orders(order_id):
    data = json.loads(request.data)
    data["id"] = order_id
    query.find_one_and_update({'id': int(order_id)} , {'$set': data})
    return f"update the post from the database"


def increment_post():
    return str(query.count_documents({}))





if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4007, debug=False)