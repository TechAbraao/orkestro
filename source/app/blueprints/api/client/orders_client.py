from source.app.schemas import uuid_schema
from source.app.extesions.socket_io import socketio
from source.app.settings.logging_settings import get_logger
from flask import Blueprint, request
from source.app.utils.responses import Response


logger = get_logger(__name__)
orders_client = Blueprint("orders_client", __name__, url_prefix="/api")

""" 01. Take all orders. """
@orders_client.route("/orders", methods=["GET"])
def get_orders(): pass

""" 02. Add a new order. """
@orders_client.route("/orders", methods=["POST"])
def post_order(): pass

""" 03. Update order. """
@orders_client.route("/orders", methods=["PUT"])
def put_order(): pass

""" 04. Delete order. """
@orders_client.route("/orders", methods=["DELETE"])
def delete_order(): pass

""" 05. Update order list on WebSocket. """
@orders_client.route("/orders/notify", methods=["POST"])
def notify_order():
    data = request.get_json()
    order_id = data.get("order_id")

    validation_query_params = uuid_schema.load({"id": order_id})
    logger.info(f"Request stored in WebSocket whose id is '{order_id}' successful.")
    socketio.emit("new_order", {"order_id": order_id})

    logger.info(f"Request received successfully at N8N, id is '{order_id}'.")
    return Response.success(
        message=f"Request whose id '{order_id}' received successfully",
        status_code=200
    )

""" 06.  """
@orders_client.route("/stores/<string:slug>/orders", methods=["POST"])
def post_order_by_slug(): pass

""" 07.  """
@orders_client.route("/stores/<string:slug>/orders/<string:order_id>", methods=["GET"])
def get_order_by_slug(): pass


