from flask import Blueprint, render_template, request, redirect, url_for
from source.app.services import menu_services
from source.app.settings.logging_settings import get_logger

logger = get_logger()
menus_client_frontend = Blueprint("menus_client_frontend", __name__, url_prefix="")

""" 1. Aqui vai renderizar os cardápios """
@menus_client_frontend.get("/menus/<string:slug>")
def view_menu_by_slug(slug: str):

    logger.info(f"Buscando menu através do slug '{slug}'")
    menu_by_slug = menu_services.get_menu_by_slug(slug)
    logger.info(f"Menu encontrado: {menu_by_slug}")
    rendering_strategy = {
        "menu_slug": slug,
        "menu_name": menu_by_slug.get("name")
    }

    return render_template("pages/client/menu_clients.jinja2", strategy=rendering_strategy)

""" 2. Aqui tem q renderizar os produtos associados às categorias dos cardápios """
@menus_client_frontend.get("/menus/<string:slug>/products/<string:product_id>")
def views_products_by_id():
    rendering_strategy = {}

    return render_template("pages/client/products_clients.jinja2", strategy=rendering_strategy)