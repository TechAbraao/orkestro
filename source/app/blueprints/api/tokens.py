from source.app.settings.logging_settings import get_logger
from source.app.services import tokens_services, stores_services, authorizations_services
from flask import request, jsonify, abort
from source.app.blueprints.routes import api
import os

logger = get_logger(__name__)
dir_name = os.path.basename(__file__)

@api.route("/tokens", methods=["POST"])
def api_generate_access_token():
    # TODO: em construção
    req = request.get_json()

    # Grant Type (OAuth) de Resource Owner Password Credentials
    if req.get("grant_type") != "password":
        abort(422, "")

    return jsonify({
        "message": "Token de acesso criado com sucesso.",
        "access_token": f""
    })

@api.route("/refresh", methods=["POST"])
def api_refresh_access_token():
    pass