from source.app.extesions.socket_io import socketio
from source.app.settings.logging_settings import get_logger
from flask import Blueprint, request, g
from source.app.utils.responses import Response
from source.app.services import menu_services, products_services, categories_services, customers_services, orders_services
from source.app.schemas import orders_schemas, uuid_schema
from source.app.blueprints.api.orders_events import broadcast_order_update
from source.app.blueprints.routes import api
import os

logger = get_logger(__name__)
dir_name = os.path.basename(__file__)

""" Capture orders from a specific Menu. """
@api.route("/orders/<string:menu_id>", methods=["GET"])
def get_orders(menu_id: str):
    logger.info(f"GET /api/orders/{menu_id} - Capture orders from a specific Menu.")

    validation_query_params = uuid_schema.load({"id": menu_id})
    orders = orders_services.get_order_by_menu_id(menu_id)
    return Response.success(
        message="Pedidos através do cardápio retornado com sucesso.",
        status_code=200,
        data=orders
    )

""" Add a new order in Menu. """
@api.route("/orders", methods=["POST"])
def post_order():

    logger.info("POST /api/orders - creating new order in menu.")
    data = request.get_json()

    """ Validando os dados do Body. """
    validating_data = orders_schemas.load(data)

    """ Campos necessários para realizar o pedido. """
    store_id = data["store_id"]
    user_id = data["user_id"]
    menu_id = data["menu_id"]
    products = data["products"]

    """ Verificar se o menu realmente existe - através do 'menu_id' """

    # logger.info(f"Verificando se o cardápio existe através do 'menu_id' = '{menu_id}'.")
    # menu_exists = menu_services.exists_menu_by_store_and_id(menu_id=menu_id, store_id=store_id)
    # if not menu_exists:
    #     return MenuFoundException("Cardápio inexistente e/ou não encontrado.")

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
    saved_order, order_identifier = orders_services.save_order_the_menu(data=data_order)
    if not saved_order:
        return Response.error(
            message="Erro ao salvar pedido no cardápio.",
            status_code=404
        )

    """ Salvar produtos associado ao pedido. """
    products_saved = orders_services.save_products_in_order(
        order_id=order_identifier,
        products=products
    )

    if not products_saved:
        return Response.error(
            message="Erro ao salvar produtos do pedido.",
            status_code=500
        )

    count_done_orders = orders_services.count_orders_done(menu_id, status="done")
    count_pending_orders = orders_services.count_orders_done(menu_id, status="pending")
    count_completed_orders = orders_services.count_orders_done(menu_id, status="completed")
    count_canceled_orders = orders_services.count_orders_done(menu_id, status="canceled")

    socketio.emit(
        "new_order",
        {
            "menu_id": menu_id,
            "orders": orders_services.get_order_by_menu_id(menu_id),
            "count_done_orders": orders_services.count_orders_done(menu_id),
            "count_pending_orders": count_pending_orders,
            "count_completed_orders": count_completed_orders,
            "count_canceled_orders": count_canceled_orders
        },
        room=menu_id
    )

    return Response.success(
        message="Novo pedido realizado com sucesso.",
        status_code=200,
        data={
            "user": customer_infos,
            "menu_id": str(menu_id),
            "status": "Done",
            "total_value": total_value,
        }
    )

""" Get order/products information  """
@api.route("/orders/<string:order_id>/products", methods=["GET"])
def get_order_infos(order_id: str):
    logger.info(f"GET /api/orders/{order_id}/products - Obter lista de produtos e informações úteis de um pedido.")

    data = []
    total_price = 0

    products_list = orders_services.get_products_in_order(order_id)
    logger.info(f"Lista de produtos retornados: {products_list}")

    for item in products_list:
        product_id = item["product_id"]
        quantity = item["quantity"]
        price = item["price"]

        product_details = products_services.get_by_id(product_id)
        product_details["quantity"] = quantity
        subtotal = price * quantity
        product_details["subtotal"] = subtotal
        total_price += subtotal

        data.append(product_details)

    logger.info(f"Lista de produtos formatados: {data}")
    logger.info(f"Total do pedido: R$ {total_price}")

    """ Obter informações do Cliente, através do ID do Cliente """
    order = orders_services.get_order_by_id(order_id)
    user_id = order.get("user_id")
    customer_infos = customers_services.find_by_id(customer_id=user_id)
    logger.info(f"Informações do Cliente: {customer_infos}")

    return Response.success(
        message="Lista de produtos do pedido.",
        status_code=200,
        data={
            "items": data,
            "total": total_price,
            "customer": customer_infos
        }
    )

""" Delete order. """
@api.route("/orders/<string:order_id>", methods=["DELETE"])
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

""" Update order status """
@api.route("/orders/<string:order_id>/status", methods=["PUT"])
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
