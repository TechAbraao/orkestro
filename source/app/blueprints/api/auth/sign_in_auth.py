from flask import Blueprint, jsonify, request, make_response
from source.app.schemas import login_stores_schemas
from source.app.utils.responses import Response
from source.app.settings.logging_settings import get_logger
from source.app.services import authorizations_services
from source.app.utils.decorators.authorizations import *

logger = get_logger(__name__)
sign_in_auth = Blueprint("sign_in_auth", __name__, url_prefix="/api/auth")

""" 1. Enter the platform """
@sign_in_auth.route("/signin", methods=["POST"])
def enter_the_platform():
    body = request.get_json()
    body_validated = login_stores_schemas.load(body)

    access_token = authorizations_services.verify_store_credentials(
        email=body["email"], password=body["password"]
    )

    resp = make_response(jsonify({
        "message": "User authenticated successfully"
    }))

    resp.set_cookie(
        "access_token",
        access_token,
        httponly=True,
        samesite="Strict",
        secure=False,
        max_age=60 * 60
    )

    return resp


@sign_in_auth.route("/logout", methods=["GET"])
@authorization_required
def end_session_store():
    resp = make_response(jsonify({"message": "User logged out successfully"}))
    resp.set_cookie(
        "access_token",
        "",
        httponly=True,
        samesite="Strict",
        secure=False,
        max_age=0
    )

    return resp
