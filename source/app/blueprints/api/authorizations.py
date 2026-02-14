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
from source.app.utils.jwt import decrypt_token
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
    redirect_to = None
    current_rule = None

    ## Cenário: Se "e-mail" e "password" forem iguais aos definidos no .env, entrará como administrador. ##
    if body["email"] == app_setiings.ADMIN_EMAIL and body["password"] == app_setiings.ADMIN_PASSWORD:
        logger.info(f"[{dir_name}] | Acessando através do administrador: {True}")

        ## Cenário: XXX
        access_token = authorizations_services.verify_store_credentials(
            email=body["email"], password=body["password"], hasAdmin=True
        )

        redirect_to = "/dashboard"
        resp = make_response(jsonify({
            "message": "User authenticated successfully",
            "redirect_to": redirect_to
        }))

        resp.set_cookie("access_token", access_token, httponly=True, samesite="Strict", secure=False, max_age=120 * 60)
        return resp

    ## Cenário: Caso não sejam as credenciais do administrador, o login será realizado normalmente. ##
    access_token = authorizations_services.verify_store_credentials(email=body["email"], password=body["password"])
    token_decrypt = decrypt_token(access_token)
    current_rule = token_decrypt.get("roles")

    if "ADMIN" in current_rule:
        redirect_to = "/dashboard"

    if "PRIVILEGED" in current_rule:
        redirect_to = "/dashboard"

    if "COMMON" in current_rule:
        redirect_to = "/orders"


    resp = make_response(jsonify({
            "message": "User authenticated successfully",
            "redirect_to": redirect_to
        }))

    resp.set_cookie("access_token", access_token, httponly=True, samesite="Strict", secure=False, max_age=120 * 60)
    return resp

@api.route("/logout", methods=["GET"])
@permissions(strategy="jwt", roles=["ADMIN", "COMMON", "PRIVILEGED"])
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
