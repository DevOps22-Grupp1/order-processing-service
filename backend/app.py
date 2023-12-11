from flask import Flask, jsonify, request, json
from prometheus_flask_exporter import PrometheusMetrics

from pymongo import MongoClient
import os

import pymongo
from pymongo import MongoClient

db_port = os.environ.get("DB_PORT")
db_username = os.environ.get("DB_USERNAME")
db_password = os.environ.get("DB_PASSWORD")
host = os.environ.get("DB_HOST")
app = Flask(__name__)
metrics = PrometheusMetrics(app)

client = MongoClient(host, 27017, username=db_username, password=db_password)

db = client.allOrders
query = db.orders


@app.route("/")
def hello_world():
    return "Success", 200, {"Access-Control-Allow-Origin": "*"}


@app.route("/api/count-products/<user_id>")
def count_product(user_id):
    count = query.count_documents({"userid": int(user_id)})
    return jsonify(count), 200, {"Access-Control-Allow-Origin": "*"}


@app.route("/api/orders", methods=["GET"])
def get_all_orders():
    data = []
    orders = db.orders.find()
    for order in orders:
        order["_id"] = str(order["_id"])
        data.append(order)
    return jsonify(data)


@app.route("/api/order/<order_id>", methods=["GET"])
def get_single_order(order_id):
    data = []
    orders = db.orders.find({"id": int(order_id)}, {"_id": 0})
    if orders:
        for order in orders:
            data.append(order)
    return jsonify(data)


@app.route("/api/order-user/<user_id>", methods=["GET"])
def get_single_order_user(user_id):
    data = []
    orders = db.orders.find({"userid": int(user_id)}, {"_id": 0})
    if orders:
        for order in orders:
            data.append(order)
    return jsonify(data)


@app.route("/api/order-product/<product_id>", methods=["GET"])
def get_single_order_product(product_id):
    data = []
    orders = db.orders.find({"productid": int(product_id)}, {"_id": 0})
    if orders:
        for order in orders:
            data.append(order)
    return jsonify(data)


@app.route("/api/order", methods=["POST"])
def post_order():
    data = json.loads(request.data)
    data["id"] = increment_order()
    db.orders.insert_one(data)
    return "A new order has been added", 201, {"Access-Control-Allow-Origin": "*"}


@app.route("/api/order/<order_id>", methods=["DELETE"])
def delete_order(order_id):
    db.orders.delete_one({"id": int(order_id)})
    return f"Deleted the order from the database"


@app.route("/api/order/<order_id>", methods=["PUT"])
def update_order(order_id):
    data = json.loads(request.data)
    data["id"] = int(order_id)
    db.orders.find_one_and_update({"id": int(order_id)}, {"$set": data})
    return f"Updated the order in the database"


def increment_order():
    return str(db.orders.count_documents({}))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=db_port, debug=False)
