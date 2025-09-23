from flask import Blueprint, render_template, request, redirect, url_for

menus_client_frontend = Blueprint("menus_client_frontend", __name__, url_prefix="")


@menus_client_frontend.get("/menus/<string:slug>")
def view_menu_by_slug(slug: str):
    return render_template("pages/menu_clients.jinja2")