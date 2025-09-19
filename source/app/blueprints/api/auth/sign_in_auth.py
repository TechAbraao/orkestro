from flask import Blueprint, jsonify, request
from source.app.schemas import login_stores_schemas
from source.app.utils.responses import Response
from source.app.services import authorizations_services

sign_in_auth = Blueprint("sign_in_auth", __name__, url_prefix="/api/auth")

""" 1. Enter the platform """
@sign_in_auth.route("/signin", methods=["POST"])
def enter_the_plataform():
    body = request.get_json()
    body_validated = login_stores_schemas.load(body)

    auth_store = authorizations_services.verify_store_credentials(
        email=body["email"], password=body["password"]
    )

    return Response.with_token(
        message="User authenticated successfully.",
        status_code=200,
        access_token="JWT_TOKEN_HERE"
    )