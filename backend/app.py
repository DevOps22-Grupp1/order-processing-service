from flask import Flask, jsonify, request, json
from prometheus_flask_exporter import PrometheusMetrics

from pymongo import MongoClient
import os

import pymongo
from pymongo import MongoClient

server_port = os.environ.get("SERVER_PORT")
db_port = os.environ.get("DB_PORT")
db_username = os.environ.get("DB_USERNAME")
db_password = os.environ.get("DB_PASSWORD")
host = os.environ.get("DB_HOST")
app = Flask(__name__)
metrics = PrometheusMetrics(app)

client = MongoClient(host, int(db_port), username=db_username, password=db_password)

db = client.allOrders
query = db.orders
cart_query = db.cart


@app.route("/")
def hello_world():
    return "Success", 200, {"Access-Control-Allow-Origin": "*"}


@app.route("/api/count-products/<user_id>")
def count_product(user_id):
    count = cart_query.count_documents({"userid": int(user_id)})
    return jsonify(count), 200, {"Access-Control-Allow-Origin": "*"}


@app.route("/api/orders", methods=["GET"])
def get_all_orders():
    data = []
    orders = query.find()
    for order in orders:
        order["_id"] = str(order["_id"])
        data.append(order)
    return jsonify(data)


@app.route("/api/order/<order_id>", methods=["GET"])
def get_single_order(order_id):
    data = []
    orders = query.find({"id": int(order_id)}, {"_id": 0})
    if orders:
        for order in orders:
            data.append(order)
    return jsonify(data)


@app.route("/api/cart/<order_id>", methods=["GET"])
def get_single_cart(order_id):
    data = []
    orders = cart_query.find({"id": int(order_id)}, {"_id": 0})
    if orders:
        for order in orders:
            data.append(order)
    return jsonify(data)


@app.route("/api/cart-user/<user_id>", methods=["GET"])
def get_single_cart_user(user_id):
    data = []
    orders = cart_query.find({"userid": int(user_id)}, {"_id": 0})
    if orders:
        for order in orders:
            data.append(order)
    return jsonify(data)


@app.route("/api/order-user/<user_id>", methods=["GET"])
def get_single_order_user(user_id):
    data = []
    orders = query.find({"userid": int(user_id)}, {"_id": 0})
    if orders:
        for order in orders:
            data.append(order)
    return jsonify(data)


@app.route("/api/order-product/<product_id>", methods=["GET"])
def get_single_order_product(product_id):
    data = []
    orders = query.find({"productid": int(product_id)}, {"_id": 0})
    if orders:
        for order in orders:
            data.append(order)
    return jsonify(data)


@app.route("/api/cart", methods=["POST"])
def post_cart():
    data = json.loads(request.data)
    data["id"] = int(increment_cart_order())
    db.cart.insert_one(data)
    return "A new order has been added", 201, {"Access-Control-Allow-Origin": "*"}


@app.route("/api/order", methods=["POST"])
def post_order():
    data = json.loads(request.data)
    data["id"] = int(increment_orders_order())
    db.orders.insert_one(data)
    return "A new order has been added", 201, {"Access-Control-Allow-Origin": "*"}


@app.route("/api/cart/<user_id>", methods=["DELETE"])
def delete_cart(user_id):
    cart_query.delete_many({"userid": int(user_id)})
    return (
        "Deleted the order from the database",
        204,
        {"Access-Control-Allow-Origin": "*"},
    )


@app.route("/api/order/<order_id>", methods=["DELETE"])
def delete_order(order_id):
    query.delete_one({"id": int(order_id)})
    return (
        "Deleted the order from the database",
        204,
        {"Access-Control-Allow-Origin": "*"},
    )


@app.route("/api/order/<order_id>", methods=["PUT"])
def update_order(order_id):
    data = json.loads(request.data)
    data["id"] = int(order_id)
    query.find_one_and_update({"id": int(order_id)}, {"$set": data})
    return f"Updated the order in the database"


def increment_cart_order():
    id_fetch = cart_query.find_one(sort=[("id", pymongo.DESCENDING)])
    if id_fetch == None:
        return "1"
    return str(id_fetch["id"] + 1)


def increment_orders_order():
    id_fetch = db.orders.find_one(sort=[("id", pymongo.DESCENDING)])
    if id_fetch == None:
        return "1"
    return str(id_fetch["id"] + 1)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=server_port, debug=False)
