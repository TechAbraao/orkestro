from source.app.schemas import stores_schemas
from source.app.services import stores_services
from source.app.blueprints.routes import api
from flask import Blueprint, jsonify, request, make_response
from source.app.schemas import login_stores_schemas
from source.app.utils.responses import Response
from source.app.settings.logging_settings import get_logger
from source.app.services import authorizations_services
from source.app.settings.application_settings import application_settings as app_setiings
from source.app.utils.decorators.authorizations import *
import os

logger = get_logger(__name__)
dir_name = os.path.basename(__file__)

@api.route("/signup", methods=["POST"])
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

@api.route("/signin", methods=["POST"])
def enter_the_platform():
    body = request.get_json()
    body_validated = login_stores_schemas.load(body)

    if body["email"] == app_setiings.ADMIN_EMAIL and body["password"] == app_setiings.ADMIN_PASSWORD:
        logger.info(f"[{dir_name}] | Acessando através do administrador: {True}")

        access_token = authorizations_services.verify_store_credentials(email=body["email"], password=body["password"], role="ADMIN", hasAdmin=True)

        resp = make_response(jsonify({"message": "User authenticated successfully"}))
        resp.set_cookie("access_token", access_token, httponly=True, samesite="Strict", secure=False, max_age=120 * 60)
        return resp

    access_token = authorizations_services.verify_store_credentials(email=body["email"], password=body["password"], role="COMMON")

    resp = make_response(jsonify({"message": "User authenticated successfully"}))
    resp.set_cookie("access_token", access_token, httponly=True, samesite="Strict", secure=False, max_age=120 * 60)

    return resp

@api.route("/logout", methods=["GET"])
@permissions(strategy="jwt", roles=["USER", "ADMIN"])
def end_session_store():
    resp = make_response(jsonify({"message": "User logged out successfully"}))
    resp.set_cookie("access_token",
        "",
        httponly=True,
        samesite="Strict",
        secure=False,
        max_age=0
    )

    return resp
