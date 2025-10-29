from source.app.schemas import uuid_schema
from source.app.extesions.socket_io import socketio
from source.app.settings.logging_settings import get_logger
from flask import Blueprint, request, g
from source.app.utils.responses import Response
from source.app.utils.decorators.authorizations import authorization_required
from source.app.services import menu_services, products_services, categories_services
from source.app.schemas import OrdersSchema

logger = get_logger(__name__)
orders_client = Blueprint("orders_client", __name__, url_prefix="/api")

""" 01. Take all orders. """
@orders_client.route("/orders", methods=["GET"])
def get_orders(): pass

""" 02. Add a new order. """
@orders_client.route("/orders", methods=["POST"])
@authorization_required
def post_order():
    store_id = g.jwt_claims.get("sub")
    logger.info("POST /api/orders - creating new order in menu.")

    data = request.get_json()

    """ Campos necessários para realizar o pedido. """
    user_id = data["user_id"] # qual usuário (o cliente)
    menu_id = data["menu_id"] # identificar qual cardápio realizou o pedido
    total_value = data["total_value"] # Essa lógica de verificar o valor total, tem que ser feita pela soma dos valores
    # dos produtos individualmente
    status = data.get("status", "pending") # status como Pendente no default

    """  """
    products = data["products"] # lista dos produtos que realizou o pedido

    """ Verificar se o menu realmente existe - através do 'menu_id' """
    logger.info(f"Verificando se o cardápio existe através do 'menu_id' = '{menu_id}'.")
    menu_exists = menu_services.exists_menu_by_store_and_id(menu_id=menu_id, store_id=store_id)
    if not menu_exists:
        return ValueError("Menu inexistente.")

    return None


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


