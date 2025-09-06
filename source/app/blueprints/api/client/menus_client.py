from source.app.utils.responses import Response
from source.app.services import menu_services

from flask import Blueprint, jsonify, abort

menus_client = Blueprint(
    "menus_client",
    __name__,
    url_prefix=""
)

@menus_client.route("/store/<string:slug>", methods=["GET"])
def render_menu_with_slug(slug: str):
    menu = menu_services.get_menu_by_slug(slug)
    return jsonify(menu)
