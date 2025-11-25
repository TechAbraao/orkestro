from flask import Blueprint, render_template, request, g, abort, redirect, url_for
from source.app.utils.decorators.authorizations import authorization_required
from source.app.settings.logging_settings import get_logger
from source.app.services import menu_services, categories_services, stores_services

main_frontend = Blueprint("main_frontend", __name__, url_prefix="")
logger = get_logger(__name__)

@main_frontend.get("/dashboard")
@authorization_required
def views_main_dashboard():
    return render_template("pages/dashboard.jinja2")

@main_frontend.get("/profile")
@authorization_required
def views_profile_dashboard():
    return render_template("pages/store_profile.jinja2")

@main_frontend.get("/orders")
@authorization_required
def views_orders_dashboard():
    store_id = g.jwt_claims.get("sub")

    menu_id = stores_services.get_menu_by_store_id(store_id)

    rendering_strategy = {
        "profile": {
            "menu_id": menu_id.get("id", ""),
        }
    }
    return render_template("pages/admin/orders.jinja2", strategy=rendering_strategy)

@main_frontend.get("/menus")
@authorization_required
def views_menus_manager_dashboard():
    store_id = g.jwt_claims.get("sub")
    logger.info(f"GET /menus - View Menu with store_id: '{store_id}'")

    """ Verificar se a Loja possui um cardápio ativo para renderizar no template. """
    hasMenu = menu_services.exists_menu_by_store_id(store_id)

    rendering_strategy = {
        "url": f"{request.path}",
        "profile": {
            "roles": f"",
            "hasMenu": hasMenu
        },
        "logged": False
    }
    return render_template("pages/manage_menu.jinja2", strategy=rendering_strategy)

@main_frontend.get("/menus/<string:menu_id>/categories")
@authorization_required
def views_edit_menu_dashboard(menu_id: str):
    store_id = g.jwt_claims.get("sub")
    logger.info(f"GET /menus/{menu_id}/edit - Visualizar categorias no menu_id: '{menu_id}'.")
    logger.info(f"UUID da Loja: {store_id}.")

    """ Verificar se o Menu/Cardápio (menu_id) existe a partir da Loja (store_id). """
    logger.info(f"Verificando se o Menu: '{menu_id}' pertence à Loja: '{store_id}'.")
    belongs_store = menu_services.exists_menu_by_store_and_id(store_id, menu_id)
    if not belongs_store:
        logger.warning(f"O Menu '{menu_id}' não pertence à Loja '{store_id}'.")
        return redirect(url_for("main_frontend.views_menus_manager_dashboard"))

    menu_info = menu_services.get_menu_by_id(menu_id)

    logger.info(f"Buscando categorias do 'menu_id' = '{menu_id}'.")
    has_categories = None
    categories_info = categories_services.get_all_categories_by_menu(menu_id)
    if categories_info:
        logger.info(f"Categoria encontrada no 'menu_id' = '{menu_id}'.")
        has_categories = True
    else:
        logger.info(f"Nenhuma categoria encontrada no 'menu_id' = '{menu_id}'.")
        has_categories = False

    rendering_strategy = {
        "profile": {
            "menu_id": menu_id,
            "menu_name": menu_info["name"],
            "hasCategories": has_categories
        }
    }

    return render_template("pages/admin/edit_menu.jinja2", strategy=rendering_strategy)