from flask import Blueprint, request, jsonify
from source.app.settings.logging_settings import get_logger
from source.app.utils.responses import Response
from source.app.blueprints.routes import api
from source.app.schemas import customers_schemas
from source.app.services import customers_services
from werkzeug.exceptions import *
import os

logger = get_logger(__name__)
dir_name = os.path.basename(__file__)

""" 1. Criar um novo Cliente/Comprador no banco de dados. """
@api.route("/customers", methods=["POST"])
def create_customer():
    logger.info("POST /api/customers - Criando um novo cliente.")

    body = request.get_json()
    logger.info("Validando os dados do Cliente.")
    validate_body = customers_schemas.load(body)

    customer_created = customers_services.add_customer(body)

    if not customer_created:
        return Response.error(
            message="Cliente já existente.",
            status_code=400
        )
    return Response.success(
        message="Novo cliente criado com sucesso.",
        status_code=200,
        data=None
    )

""" 2. Busca um cliente através do seu ID (UUID type) ou telefone """
@api.route("/customers", methods=["GET"])
def get_customer():
    """
    Buscar cliente por ID ou por telefone usando query params:
    /customers?id=<customer_id>
    /customers?telephone=<telephone_number>
    """

    customer_id = request.args.get("id")
    telephone = request.args.get("telephone")

    if customer_id:
        logger.info(f"Buscando cliente pelo ID: {customer_id}")
        data = customers_services.find_by_id(customer_id)
        if not data:
            return Response.error(
                message="Cliente não encontrado pelo ID.",
                status_code=404
            )
        return Response.success(
            message="Cliente encontrado com sucesso.",
            status_code=200,
            data=data
        )

    elif telephone:
        logger.info(f"Buscando cliente pelo telefone: {telephone}")
        user_id = customers_services.find_user_id_by_telephone(telephone)
        if not user_id:
            return Response.error(
                message="Cliente não encontrado pelo telefone.",
                status_code=404
            )
        return Response.success(
            message="Cliente encontrado com sucesso.",
            status_code=200,
            data={"user_id": user_id}
        )

    else:
        return Response.error(
            message="É necessário informar 'id' ou 'telephone' como query param.",
            status_code=400
        )

