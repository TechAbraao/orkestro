from source.app.services import menu_services
from source.app.services import categories_services
from flask import Blueprint, jsonify, abort
from source.app.schemas import uuid_schema

menus_client = Blueprint(
    "menus_client",
    __name__,
    url_prefix=""
)

@menus_client.route("/stores/<string:slug>", methods=["GET"])
def render_menu_with_slug(slug: str):
    menu = menu_services.get_menu_by_slug(slug)
    return jsonify(menu)

@menus_client.route("/stores/<string:slug>/categories/<string:category_id>", methods=["GET"])
def get_category(slug: str, category_id: str):
    validation_query_params = uuid_schema.load({"id": category_id})

    category = categories_services.get_category_by_id_and_slug(
        category_id=validation_query_params["id"],
        slug=slug
    )

    return jsonify(category)