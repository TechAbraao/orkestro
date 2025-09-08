from source.app.utils.responses import Response
from source.app.schemas import uuid_schema
from source.app.extesions.socket_io import socketio

from flask import Blueprint, request

orders_client = Blueprint(
    "orders_client",
    __name__,
    url_prefix="/api"
)

@orders_client.route("/orders/notify", methods=["POST"])
def notify_order():
    data = request.get_json()
    order_id = data.get("order_id")

    validation_query_params = uuid_schema.load({"id": order_id})
    socketio.emit("new_order", {"order_id": order_id})

    return {"message": f"Pedido {order_id} recebido com sucesso!"}, 200