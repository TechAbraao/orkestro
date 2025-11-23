from flask import Blueprint, request, jsonify
from source.app.utils.responses import Response
from source.app.schemas import stores_schemas
from source.app.services import stores_services

sign_up_auth = Blueprint("sign_up_auth", __name__, url_prefix="/api/auth")

""" 1. Create a new account """
@sign_up_auth.route("/signup", methods=["POST"])
def create_new_account():
    body = request.get_json()
    body_validated = stores_schemas.load(body)

    created = stores_services.create_new_account(body)
    if not created:
        return Response.error(
            message="Erro ao criar loja.",
            status_code=400
        )

    return Response.success(
        message="Loja criada com sucesso.",
        status_code=200
    )
