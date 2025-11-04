from source.app.schemas import uuid_schema
from source.app.extesions.socket_io import socketio
from source.app.settings.logging_settings import get_logger
from flask import Blueprint, request, g
from source.app.utils.responses import Response
from source.app.utils.decorators.authorizations import authorization_required
from source.app.exceptions.menu_exceptions import *
from source.app.services import menu_services, products_services, categories_services, customers_services, orders_services
from source.app.schemas import orders_schemas, uuid_schema
from source.app.blueprints.api.client.orders_events_client import broadcast_order_update

logger = get_logger(__name__)
orders_client = Blueprint("orders_client", __name__, url_prefix="/api")

""" 01. Capture orders from a specific Menu. """
@orders_client.route("/orders/<string:menu_id>", methods=["GET"])
def get_orders(menu_id: str):
    logger.info(f"GET /api/orders/{menu_id} - Capture orders from a specific Menu.")

    validation_query_params = uuid_schema.load({"id": menu_id})
    orders = orders_services.get_order_by_menu_id(menu_id)
    return Response.success(
        message="Pedidos através do cardápio retornado com sucesso.",
        status_code=200,
        data=orders
    )

""" 02. Add a new order in Menu. """
@orders_client.route("/orders", methods=["POST"])
@authorization_required
def post_order():
    store_id = g.jwt_claims.get("sub")
    logger.info("POST /api/orders - creating new order in menu.")
    data = request.get_json()

    """ Validando os dados do Body. """
    validating_data = orders_schemas.load(data)

    """ Campos necessários para realizar o pedido. """
    user_id = data["user_id"]
    menu_id = data["menu_id"]
    products = data["products"]

    """ Verificar se o menu realmente existe - através do 'menu_id' """
    logger.info(f"Verificando se o cardápio existe através do 'menu_id' = '{menu_id}'.")
    menu_exists = menu_services.exists_menu_by_store_and_id(menu_id=menu_id, store_id=store_id)
    if not menu_exists:
        return MenuFoundException("Cardápio inexistente e/ou não encontrado.")

    """ Obter informações do Cliente. """
    customer_infos = customers_services.find_by_id(customer_id=user_id)
    logger.info(f"Informações do Cliente: {customer_infos}")

    """ Verificar se os produtos existem e operações realizados a lógica do Cardápio. """
    logger.info(f"Informações dos Produtos: {products}")
    total_value = 0

    for item in products:
        product_id = item["product_id"]
        quantity = item["quantity"]

        """ Buscar infos do Produto. """
        find_product = products_services.get_by_id(product_id)

        if not find_product:
            return Response.error(
                message=f"Produto com ID {product_id} não encontrado.",
                status_code=404
            )
        product_price = find_product.get("price", 0)
        logger.info(f"Produto de ID: '{product_id}' tem preço igual: R$ {product_price}")

        """ Somar ao valor total """
        total_value += product_price * quantity
    logger.info(f"Valor total do pedido: R$ {total_value}")

    data_order = {
        "menu_id": menu_id,
        "total_value": total_value,
        "user_id": user_id,
        "name": customer_infos["name"],
        "telephone": customer_infos["telephone"],
        "status": "done",
    }

    """ Salvar pedido referente ao cardápio. """
    saved = orders_services.save_order_the_menu(data=data_order)
    if not saved:
        return Response.error(
            message="Erro ao salvar pedido no cardápio.",
            status_code=404
        )

    socketio.emit(
        "new_order",
        {"menu_id": menu_id, "orders": orders_services.get_order_by_menu_id(menu_id)},
        room=menu_id
    )

    return Response.success(
        message="Novo pedido realizado com sucesso.",
        status_code=200,
        data={
            "user": customer_infos,
            "menu_id": str(menu_id),
            "products": None,
            "status": "Done",
            "total_value": total_value
        }
    )

""" 03. Delete order. """
@orders_client.route("/orders/<string:order_id>", methods=["DELETE"])
def delete_order(order_id: str):
    logger.info(f"DELETE /api/orders - Deletar um pedido através do cardápio")

    """ Query Params do ID do Cardápio. """
    """ Nesse cenário, o 'menu_id' é obrigatório. """
    menu_id = request.args.get("menu_id")
    if not menu_id:
        return Response.error(
            message="Erro ao selecionar cardápio.",
            status_code=400
        )
    if menu_id:
        uuid_schema.load({"id": menu_id})

    """ Validar UUID do Pedido e Cardápio. """
    # validation_query_params_menu_id = uuid_schema.load({"id": menu_id})
    validation_query_params_order_id = uuid_schema.load({"id": order_id})

    order_deleted = orders_services.delete_order_by_id(order_id)
    if not order_deleted:
        return Response.error(
            message="Erro ao deletar pedido.",
            status_code=404
        )

    """ Notificar o WebSocket """
    socketio.emit(
        "new_order",
        {"menu_id": menu_id, "orders": orders_services.get_order_by_menu_id(menu_id)},
        room=menu_id
    )

    """ Resposta da API (Deletar). """
    return Response.success(
        message="Pedido deletado com sucesso.",
        status_code=200
    )

""" 04. Update order. """
@orders_client.route("/orders", methods=["PUT"])
def put_order(): pass

""" 05. Update order list on WebSocket. """
@orders_client.route("/orders/notify", methods=["POST"])
def notify_order():
    data = request.get_json()
    menu_id = data.get("menu_id")

    validation_query_params = uuid_schema.load({"id": menu_id})
    all_orders = orders_services.get_order_by_menu_id(menu_id=menu_id)
    logger.info(f"Request stored in WebSocket whose id is '{menu_id}' successful.")
    logger.info(f"Orders in Menu: {all_orders}")
    socketio.emit("new_order", {"order_id": all_orders})

    logger.info(f"Request received successfully at N8N, id is '{menu_id}'.")
    return Response.success(
        message=f"Request whose id '{menu_id}' received successfully",
        status_code=200,
    )

""" 06. Update order status """
@orders_client.route("/orders/<string:order_id>/status", methods=["PUT"])
def order_status(order_id):
    logger.info(f"PUT /api/orders/{order_id}/status - Atualizar status do pedido")

    body = request.get_json()
    status = body.get("status")

    status_accepts = ["done", "pending", "completed", "canceled"]
    if status not in status_accepts:
        return Response.error(
            message="Status inválido. Os status permitidos são: done, pending, completed, canceled.",
            status_code=400
        )

    menu_id = request.args.get("menu_id")
    if not menu_id:
        return Response.error(
            message="Erro ao selecionar cardápio.",
            status_code=400
        )
    if menu_id:
        uuid_schema.load({"id": menu_id})

    updated = orders_services.update_order_status(status, order_id)
    if not updated:
        return Response.error(
            message="Erro ao atualizar status do pedido.",
            status_code=400
        )

    """ Notificar o WebSocket da atualização do status. """
    broadcast_order_update(menu_id, updated)

    return Response.success(
        message="Status atualizado com sucesso.",
        status_code=200,
        data=updated
    )