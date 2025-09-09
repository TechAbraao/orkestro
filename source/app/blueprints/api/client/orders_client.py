from source.app.schemas import uuid_schema
from source.app.extesions.socket_io import socketio

from flask import Blueprint, request

orders_client = Blueprint(
    "orders_client",
    __name__,
    url_prefix="/api"
)

""" 1. Take all orders. """
@orders_client.route("/orders", methods=["GET"])
def get_orders(): pass

""" 2. Add a new order. """
@orders_client.route("/orders", methods=["POST"])
def post_order(): pass

""" 3. Update order. """
@orders_client.route("/orders", methods=["PUT"])
def put_order(): pass

""" 4. Delete order. """
@orders_client.route("/orders", methods=["DELETE"])
def delete_order(): pass

""" 5. Update order list on WebSocket. """
@orders_client.route("/orders/notify", methods=["POST"])
def notify_order():
    data = request.get_json()
    order_id = data.get("order_id")

    validation_query_params = uuid_schema.load({"id": order_id})
    socketio.emit("new_order", {"order_id": order_id})

    return {"message": f"Pedido {order_id} recebido com sucesso!"}, 200

""" 6.  """
@orders_client.route("/stores/<string:slug>/orders", methods=["POST"])
def post_order_by_slug(): pass

""" 7.  """
@orders_client.route("/stores/<string:slug>/orders/<string:order_id>", methods=["GET"])
def post_order_by_slug(): pass


