from flask import Blueprint, request, jsonify
from source.app.utils.responses import Response
from source.app.schemas import menu_schema, uuid_schema
from source.app.services import menu_services
from source.app.settings.logging_settings import get_logger

logger = get_logger(__name__)
menus_bp = Blueprint("menus_bp", __name__, url_prefix="/api/menus")

""" 1. Criar um Cardápio """
@menus_bp.route("/", methods=["POST"])
def create_menu():
    logger.info("POST /menus - creating new menu")

    logger.info("Getting JSON data from request and validating fields")
    data = request.get_json()
    data_validated = menu_schema.load(data)


    created = menu_services.create_menu(data_validated)

    logger.info(f"Menu created successfully")
    return Response.success(
        message="Menu created successfully.",
        status_code=200,
        data=None,
    )

""" 2. Listar todos os Cardápios """
@menus_bp.route("/", methods=["GET"])
def all_menus():
    logger.info("GET /menus - retrieving all menus.")

    include = request.args.get("include", "").lower().split(",")
    all_menus_returned = menu_services.get_all_menus(include=include)

    logger.info("All menus returned,")
    return jsonify(all_menus_returned)

""" 3. Deletar um Cardápio """
@menus_bp.route("/<string:menu_id>", methods=["DELETE"])
def delete_menu(menu_id: str):
    logger.info("DELETE /menus/<menu_id> - deleting a menu")

    uuid_schema.load({"id": menu_id})
    menu_services.delete_menu(menu_id)

    return Response.success(
        message="Menu deleted successfully.",
        status_code=200
    )


""" 4. Atualizar um Cardápio """
@menus_bp.route("/<string:menu_id>", methods=["PUT"])
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