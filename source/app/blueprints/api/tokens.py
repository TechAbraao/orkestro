from source.app.settings.logging_settings import get_logger
from source.app.services.tokens_services import TokensServices
from source.app.utils.responses import *
from flask import request, jsonify, g
from source.app.blueprints.routes import api
import os

logger = get_logger(__name__)
dir_name = os.path.basename(__file__)

@api.before_request
def setup_token():
    if request.path == "/api/tokens" and request.method == "POST":
        g.tokens_services = TokensServices()

@api.route("/tokens", methods=["POST"])
def api_generate_access_token():
    data = request.get_json() or {}
    store_id = data.get("store_id")

    if not store_id:
        return jsonify({"error": "store_id is required"}), 400

    token = g.tokens_services.generate_access_token(store_id)

    return jsonify({
        "message": "Token de acesso criado com sucesso.",
        "access_token": f"{token}"
    })

@api.route("/refresh", methods=["POST"])
def api_refresh_access_token():
    pass