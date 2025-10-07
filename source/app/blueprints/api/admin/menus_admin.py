from flask import Blueprint, request, jsonify, g
from source.app.utils.responses import Response
from source.app.schemas import menu_schema, uuid_schema
from source.app.services import menu_services
from source.app.settings.logging_settings import get_logger
from source.app.utils.decorators.authorizations import authorization_required
from werkzeug.exceptions import *

logger = get_logger(__name__)
menus_bp = Blueprint("menus_bp", __name__, url_prefix="/api/menus")

""" 1. Criar um novo Menu. """
@menus_bp.route("/", methods=["POST"])
@authorization_required
def create_menu():
    store_id = g.jwt_claims.get("sub")
    logger.info(f"POST /menus - creating new menu in store_id: '{store_id}'")

    data = request.get_json()
    data_validated = menu_schema.load(data)

    data_validated["store_id"] = store_id
    created = menu_services.create_menu(data_validated)

    return Response.success(
        message="Menu created successfully.",
        status_code=200,
        data=None,
    )

""" 2. Obter menus (do usuário autenticado ou todos). """
@menus_bp.route("/", methods=["GET"])
@authorization_required
def get_menus():
    logger.info("GET /menus ou /menus?mine=true - Retornando todos os menus.")

    """ Caso o usuário queira os menus da própria loja (precisa estar autenticado). """
    only_my_store = request.args.get("mine", "false").lower() == "true"

    if only_my_store:
        store_id = g.jwt_claims.get("sub")
        logger.info(f"Retornando os menus da loja autenticada. UUID da loja: '{store_id}'. ")

        menus = menu_services.get_menus_by_store_id(store_id)
        return Response.success(
            message="Menus returned successfully (by store).",
            status_code=200,
            data=menus
        )
    else:
        logger.info("Retornando todos os menus disponíveis.")
        include = request.args.get("include", "").lower().split(",")
        all_menus_returned = menu_services.get_all_menus(include=include)
        return jsonify(all_menus_returned)

""" 3. Deletar Menu. """
@menus_bp.route("/<string:menu_id>", methods=["DELETE"])
@authorization_required
def delete_menu(menu_id: str):
    logger.info("DELETE /menus/<menu_id> - deleting a menu")

    uuid_schema.load({"id": menu_id})
    menu_services.delete_menu(menu_id)

    return Response.success(
        message="Menu deleted successfully.",
        status_code=200
    )

""" 4. Atualizar Menu. """
@menus_bp.route("/<string:menu_id>", methods=["PUT"])
@authorization_required
def update_menu(menu_id: str):
    logger.info("PUT /menus/<menu_id> - updating a menu")

    logger.info("Getting JSON data from request and validating fields")
    data = request.get_json()

    uuid_schema.load({"id": menu_id})
    data_validated = menu_schema.load(data)

    menu_services.update_menu(menu_id, data_validated)

    return Response.success(
        message="Menu updated successfully.",
        status_code=200
    )


""" 5. Atualizar status do cardápio (ativado/desativado). """
@menus_bp.route("/<string:menu_id>/status", methods=["PATCH"])
@authorization_required
def change_status_menu(menu_id: str):
    store_id = g.jwt_claims.get("sub")
    logger.info(f"PATCH /menus/{menu_id}/status - Atualizando o status do cardápio.")

    logger.info(f"Verificando se o menu_id = '{menu_id}' existe no store_id = '{store_id}'.")
    menu_exists_in_store = menu_services.exists_menu_by_store_and_id(menu_id=menu_id, store_id=store_id)

    if not menu_exists_in_store:
        logger.warning(f"O menu_id '{menu_id}' não existe no store_id '{store_id}'.")
        return Response.error(message="Menu não encontrado.", status_code=404)

    logger.info("Iniciando o processo de alternância do status do cardápio.")
    new_status = menu_services.change_status_menu(menu_id=menu_id)

    return Response.success(
        message=f"Status atualizado para {'ativo' if new_status else 'inativo'}.",
        status_code=200
    )


""" 6. Ver o status atual do cardápio (ativado/desativado). """
@menus_bp.route("/<string:menu_id>/status", methods=["GET"])
@authorization_required
def get_status_menu(menu_id: str):
    store_id = g.jwt_claims.get("sub")
    logger.info(f"GET /menus/{menu_id}/status - Obtendo estado atual do cardápio (ativado/desativado).")

    # logger.info(f"Verificando se o menu_id = '{menu_id}' existe no store_id = '{store_id}'.")
    # menu_exists_in_store = menu_services.exists_menu_by_store_and_id(menu_id=menu_id, store_id=store_id)

    menu = menu_services.get_menu_by_id(menu_id=menu_id)
    logger.info(f"menu_id = {menu_id} encontrado: {menu}")


    return Response.success(
        message="Status atual do cardápio retornado.",
        data=menu.get("activated"),
        status_code=200
    )

