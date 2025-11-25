from source.app.services import menu_services
from source.app.services import categories_services
from flask import Blueprint, jsonify
from source.app.schemas import uuid_schema
from source.app.utils.responses import Response
from source.app.settings.logging_settings import get_logger

logger = get_logger(__name__)

menus_client = Blueprint("menus_client", __name__, url_prefix="/api")

""" 01. X """
@menus_client.route("/stores/<string:slug>", methods=["GET"])
def render_menu_with_slug(slug: str):
    menu = menu_services.get_menu_by_slug(slug)
    logger.info(f"Status do menu: {menu.get("activated")}")

    return Response.success(
        message="Menu returned successfully.",
        data=menu,
        status_code=200
    )

@menus_client.route("/stores/<string:slug>/details", methods=["GET"])
def menu_with_slug_details(slug: str):
    menu_details = menu_services.get_menu_details_by_slug(slug)
    return Response.success(
        message="Detalhes do menu retornado com sucesso.",
        data=menu_details,
        status_code=200
    )

""" 02. X """
@menus_client.route("/stores/<string:slug>/categories/<string:category_id>", methods=["GET"])
def get_category(slug: str, category_id: str):
    validation_query_params = uuid_schema.load({"id": category_id})

    category = categories_services.get_category_by_id_and_slug(
        category_id=validation_query_params["id"],
        slug=slug
    )

    return jsonify(category)