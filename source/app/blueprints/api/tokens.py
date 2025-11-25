from flask import request, jsonify
from source.app.settings.logging_settings import get_logger
from source.app.blueprints.routes import api

logger = get_logger(__name__)
dir_name = 'tokens.py'

@api.route("/token", methods=["GET"])
def api_get_token():
    return jsonify({
        "access_token": ""
    })
