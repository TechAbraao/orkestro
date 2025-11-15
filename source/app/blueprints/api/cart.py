from flask import render_template, request, abort, redirect, url_for, session, g
from source.app.blueprints.routes import api
from source.app.settings.logging_settings import get_logger

logger = get_logger(__name__)

""" Em construção -- IDEALIZANDO"""
@api.route("/cart/validate-cart", methods=["POST"])
def api_validate_cart():
    body = request.get_json()

    """" Estudar a fundo essa proposta de vir o category_id """
    """ Em casos de sobrecarregar o servidor """
    cart = body.get("cart")
    category_id = body.get("category_id")

    logger.info(f"UUID da categoria para retornar: {category_id}")
    if not cart or not cart.get("products"):
        return {"error": "Cart empty"}, 400

    session["return_id"] = category_id
    return {"ok": True}, 200
