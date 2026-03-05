from flask import Blueprint, request, jsonify, g
from source.app.utils.responses import Response
from source.app.schemas import menu_schema, uuid_schema, opening_hours_schemas
from source.app.services import (menu_services, opening_hours_services, categories_services)
from source.app.settings.logging_settings import get_logger
from source.app.utils.decorators.authorizations import api_permissions
from werkzeug.exceptions import *
from source.app.blueprints.routes import api
import os

logger = get_logger(__name__)
dir_name = os.path.basename(__file__)

""" 01. Criar um novo Menu (Cardápio). """
@api.route("/menus", methods=["POST"])
@api_permissions(strategy="jwt", roles=["ADMIN", "PRIVILEGED"])
def create_menu():
    store_id = g.jwt_claims.get("sub")
    logger.info(f"POST /menus - creating new menu in store_id: '{store_id}'")

    data = request.get_json()
    roles = data.get("roles")
    data_validated = menu_schema.load(data)


    roles_accepts = ["VIEWER", "COMMON"]
    if roles not in roles_accepts:
         abort(400, description="Invalid menu rule. Only the following are valid: ['VIEWER'] or ['COMMON']")


    data_validated["store_id"] = store_id
    created = menu_services.create_menu(data_validated)

    return Response.success(
        message="Menu created successfully.",
        status_code=200,
        data=None,
    )

""" 02. Obter menus (do usuário autenticado ou todos). """
@api.route("/menus", methods=["GET"], strict_slashes=False)
@api_permissions(strategy="jwt", roles=["ADMIN", "COMMON", "PRIVILEGED"])
def get_menus():
    logger.info("GET /menus ou /menus?mine=true - Retornando todos os menus.")

    """ Caso o usuário queira os menus da própria loja (precisa estar autenticado). """
    only_my_store = request.args.get("mine", "false").lower() == "true"

    if only_my_store:
        store_id = g.jwt_claims.get("sub")
        logger.info(f"Retornando os menus da loja autenticada. UUID da loja: '{store_id}'. ")

        menus = menu_services.get_menus_by_store_id(store_id)
        print(menus)


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

""" 03. Deletar Menu (Cardápio). """
@api.route("/menus/<string:menu_id>", methods=["DELETE"])
@api_permissions(strategy="jwt", roles=["ADMIN", "PRIVILEGED"])
def delete_menu(menu_id: str):
    logger.info("DELETE /menus/<menu_id> - deleting a menu")

    uuid_schema.load({"id": menu_id})
    menu_services.delete_menu(menu_id)

    return Response.success(
        message="Menu deleted successfully.",
        status_code=200
    )

""" 04. Atualizar Menu (Cardápio). """
@api.route("/menus/<string:menu_id>", methods=["PUT"])
@api_permissions(strategy="jwt", roles=["ADMIN", "COMMON", "PRIVILEGED"])
def update_menu(menu_id: str):
    logger.info("PUT /menus/<menu_id> - updating a menu")

    logger.info("Getting JSON data from request and validating fields")
    data = request.get_json()

    uuid_schema.load({"id": menu_id})
    data_validated = menu_schema.load(data)

    roles = data.get("roles", None)
    roles_accepts = ["VIEWER", "COMMON"]
    if roles not in roles_accepts:
        abort(400, description="Invalid menu rule. Only the following are valid: ['VIEWER'] or ['COMMON']")

    menu_services.update_menu(menu_id, data_validated)

    return Response.success(
        message="Menu updated successfully.",
        status_code=200
    )

""" 05. Atualizar status do Menu (Cardápio) (ativado/desativado). """
@api.route("/menus/<string:menu_id>/status", methods=["PATCH"])
@api_permissions(strategy="jwt", roles=["ADMIN", "COMMON", "PRIVILEGED"])
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

""" 06. Ver o status atual do cardápio (ativado/desativado). """
@api.route("/menus/<string:menu_id>/status", methods=["GET"])
@api_permissions(strategy="jwt", roles=["ADMIN", "COMMON", "PRIVILEGED"])
def get_status_menu(menu_id: str):
    store_id = g.jwt_claims.get("sub")
    logger.info(f"GET /menus/{menu_id}/status - Obtendo estado atual do cardápio (ativado/desativado).")

    menu = menu_services.get_menu_by_id(menu_id=menu_id)
    logger.info(f"menu_id = {menu_id} encontrado: {menu}")

    return Response.success(
        message="Status atual do cardápio retornado.",
        data=menu.get("activated"),
        status_code=200
    )

""" 07. Adicionar horário de funcionamento do Menu (Cardápio) """
@api.route("/menus/<string:menu_id>/opening-hours", methods=["POST"])
def save_opening_hours(menu_id):
    logger.info(f"POST /api/menus/{menu_id}/opening-hours - Salvando todos os horários de funcionamento de um cardápio.")

    DAYS_OF_WEEK = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    data = request.get_json()

    received_days = [item["day"].lower() for item in data]
    missing_days = [day for day in DAYS_OF_WEEK if day not in received_days]
    if missing_days:
        return Response.error(
            message=f"Missing days in request: {', '.join(missing_days)}",
            status_code=400,
            data=None
        )

    data_validated = opening_hours_schemas.load(data, many=True)
    logger.info(f"Body da Request: {opening_hours_schemas.dump(data_validated, many=True)}")

    saved = opening_hours_services.save_hours_in_menu(menu_id=menu_id, data=data)
    logger.info(f"menu_id: '{menu_id}' - Horário de funcionamento adicionado: {saved}")

    if not saved:
        return Response.error(
            message="Error saving opening hours.",
            status_code=BadRequest.code
        )
    return Response.success(
        message="Opening hours added successfully.",
        status_code=201,
        data=data
    )

""" 08. Pegar o horário de funcionamento do Menu (Cardápio) """
@api.route("/menus/<string:menu_id>/opening-hours", methods=["GET"])
def get_opening_hours(menu_id):
    logger.info(f"GET /api/menus/{menu_id}/opening-hours - Obtendo todos os horários de funcionamento de um cardápio.")

    hours_opening = opening_hours_services.get_menu_opening_hours(menu_id)
    logger.info(f"Horários do menu_id '{menu_id}' foram encontrados: {hours_opening}")

    return Response.success(
        message="All times returned successfully.",
        status_code=200,
        data=hours_opening
    )

""" 09. Atualizar o horário de funcionamento do Menu (Cardápio) """
@api.route("/menus/<string:menu_id>/opening-hours", methods=["PUT"])
def update_opening_hours(menu_id):
    pass

""" 10. Deletar o horário de funcionamento do Menu (Cardápio) """
@api.route("/menus/<string:menu_id>/opening-hours", methods=["DELETE"])
def delete_opening_hours(menu_id):
    logger.info(f"DELETE /api/menus/{menu_id}/opening-hours - Deletando TODOS os horários de funcionamento do cardápio.")

    all_deleted = opening_hours_services.delete_all_hours(menu_id=menu_id)
    if not all_deleted:
        return Response.error(
            message="Error deleting all menu times.",
            status_code=NotFound.code
        )
    return Response.success(
        message="All opening hours deleted successfully.",
        status_code=200
    )

@api.route("/stores/<string:slug>", methods=["GET"])
def render_menu_with_slug(slug: str):
    menu = menu_services.get_menu_by_slug(slug)

    logger.info(f"Status do menu: {menu.get("activated")}")

    return Response.success(
        message="Menu returned successfully.",
        data=menu,
        status_code=200
    )

@api.route("/stores/<string:slug>/details", methods=["GET"])
def menu_with_slug_details(slug: str):
    menu_details = menu_services.get_menu_details_by_slug(slug)
    return Response.success(
        message="Detalhes do menu retornado com sucesso.",
        data=menu_details,
        status_code=200
    )

""" 02. X """
@api.route("/stores/<string:slug>/categories/<string:category_id>", methods=["GET"])
def get_category(slug: str, category_id: str):
    validation_query_params = uuid_schema.load({"id": category_id})

    category = categories_services.get_category_by_id_and_slug(
        category_id=validation_query_params["id"],
        slug=slug
    )

    return jsonify(category)