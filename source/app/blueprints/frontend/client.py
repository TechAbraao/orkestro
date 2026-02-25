from flask import render_template, url_for, g, session, abort
from source.app.exceptions.menu_exceptions import MenuNotFoundException
from source.app.utils.fallbacks import find_similar_menu_slug
from source.app.services import menu_services, categories_services, stores_services
from source.app.settings.logging_settings import get_logger
from source.app.blueprints.routes import vws
import os

logger = get_logger()
dir_name = os.path.basename(__file__)

""" 1. Esta parte do código é responsável por renderizar todos os cardápios disponíveis na interface. """
@vws.get("/menus/<string:slug>")
def view_menu_by_slug(slug: str):
    logger.info(f"[{dir_name}] Buscando menu pelo slug: {slug}")

    try:
        menu_by_slug = menu_services.get_menu_by_slug(slug)
    except MenuNotFoundException as e:
        all_slugs = menu_services.get_all_menu_slugs()
        logger.info(f"[{dir_name}] | Todos os slugs encontrados: {all_slugs}")
        suggestion = find_similar_menu_slug(
            slug,
            all_slugs
        )
        logger.info(f"[{dir_name}] | Menu não encontrado. Sugestão gerada: '{suggestion}'")
        return render_template("errors/menu_not_found.jinja2", suggestion=suggestion), 404

    menu_id = menu_by_slug["id"]

    verify_category = categories_services.get_all_categories_by_menu(menu_id)

    hasCategory = False
    if verify_category:
        hasCategory = True
    else:
        hasCategory = False

    rendering_strategy = {
        "menu_slug": slug,
        "menu_id": menu_id,
        "menu_name": menu_by_slug.get("name"),
        "has_category": bool(hasCategory),
        "menu_roles": menu_by_slug["roles"]
    }

    return render_template("pages/menu_clients.jinja2", strategy=rendering_strategy)

""" 2. Aqui será feita a renderização dos produtos pertencentes às categorias dos cardápios. """
@vws.get("/menus/<string:slug>/<string:category_id>")
def views_category_by_id(slug: str, category_id: str):

    logger.info(f"Buscando menu através do slug '{slug}'")
    menu_by_slug = menu_services.get_menu_by_slug(slug)
    logger.info(f"Menu encontrado: {menu_by_slug}")
    print("Suas rOles do menu: ", menu_by_slug["roles"])
    logger.info(f"Buscando informações da categoria")
    category_info = categories_services.get_category_by_id(category_id)

    store = stores_services.get_store_by_slug(slug)
    menu_id = store.get("id")

    rendering_strategy = {
        "menu_slug": slug,
        "menu_name": menu_by_slug.get("name"),
        "menu_id": menu_id,
        "category_id": category_id,
        "category_name": category_info.get("name"),
        "menu_roles": menu_by_slug["roles"]
    }

    return render_template("pages/category_clients.jinja2", strategy=rendering_strategy)

""" 3. Aqui será feito a renderização do produto em específico que pertence a categoria do cardápio.  """
@vws.get("/menus/<string:slug>/products/<string:product_id>")
def views_product_by_id(slug: str, product_id: str):
    logger.info(f"Buscando menu através do slug '{slug}'")
    menu_by_slug = menu_services.get_menu_by_slug(slug)
    logger.info(f"Menu encontrado: {menu_by_slug}")

    rendering_strategy = {
        "menu_slug": slug,
        "menu_name": menu_by_slug.get("name"),
        # "category_id": menu_by_slug.get("id"),
        "product_id": product_id
    }

    return render_template("pages/products_details_clients.jinja2", strategy=rendering_strategy)

@vws.route("/menus/<string:slug>/cart", methods=["GET"])
def vws_payment_order(slug: str):
    g.return_id = session.get("return_id", "N/A")
    logger.info(f"Return UUID para retornar a categoria certa: {g.return_id}")
    """ Return UUID identifica e avisa o front-end qual é o cardapio pra retornar """
    rendering_strategy = {
        "menu_slug": slug,
        "return_id": g.return_id
    }
    return render_template("pages/cart.jinja2", strategy=rendering_strategy)

@vws.route("/menus/<string:slug>/payment", methods=["GET"])
def vws_finalize_order(slug: str):
    rendering_strategy = {
        "menu_slug": slug,
    }
    return render_template("pages/finalize_order.jinja2", strategy=rendering_strategy)

