from flask import Blueprint, request, jsonify
from source.app.settings.logging_settings import get_logger
from source.app.utils.responses import Response
from source.app.schemas import customers_schemas
from source.app.services import customers_services
from werkzeug.exceptions import *

logger = get_logger(__name__)

customers = Blueprint("customers", __name__, url_prefix="/api")

""" 1. Criar um novo Cliente/Comprador no banco de dados. """
@customers.route("/customers", methods=["POST"])
def create_customer():
    logger.info("POST /api/customers - Criando um novo cliente.")

    body = request.get_json()
    logger.info("Validando os dados do Cliente.")
    validate_body = customers_schemas.load(body)

    customer_created = customers_services.add_customer(body)

    if not customer_created:
        return Response.error(
            message="Erro ao criar cliente.",
            status_code=400
        )
    return Response.success(
        message="Novo cliente criado com sucesso.",
        status_code=200,
        data=None
    )

""" 2. Buscar um Cliente através do seu ID. """
@customers.route("/customers/<string:customer_id>", methods=["GET"])
def search_customer(customer_id: str):
    logger.info(f"GET /api/customers/{customer_id} - Buscando cliente através do ID.")

    data = customers_services.find_by_id(customer_id=customer_id)
    if not data:
        return Response.error(
            message="Erro ao buscar cliente.",
            status_code=NotFound.code
        )
    return Response.success(
        message="Cliente encontrado com sucesso.",
        status_code=200,
        data=data
    )

""" 3. """


""" 4. """