from flask import Blueprint, render_template, request, redirect, url_for, g
from source.app.utils.decorators.authorizations import authenticated, permissions
from source.app.services import stores_services

from source.app.blueprints.routes import vws

@vws.get("/")
@authenticated
def views_root():
    return redirect(url_for("vws.views_homepage"))

@vws.get("/home")
@authenticated
def views_homepage():
    rendering_strategy = {
        "url": f"{request.path}",
        "profile": {
            "roles": f""
        },
        "logged": False
    }
    return render_template("/pages/homepage.jinja2", strategy=rendering_strategy)

@vws.get("/signin")
@authenticated
def views_login():

    rendering_strategy = {
        "url": f"{request.path}",
        "profile": {
            "roles": f""
        },
        "logged": False
    }

    return render_template("pages/signin.jinja2", strategy=rendering_strategy)

@vws.get("/accounts")
@permissions(strategy="jwt", roles=["ADMIN"])
def views_register():
    store_id = g.jwt_claims.get("sub")
    roles = g.jwt_claims.get("roles")
    menu_id = stores_services.get_menu_by_store_id(store_id)

    rendering_strategy = {
        "url": f"{request.path}",
        "profile": {
            "roles": roles,
            "menu_id": menu_id.get("id"),
        },
        "logged": False,
    }

    return render_template("pages/accounts.jinja2", strategy=rendering_strategy)
