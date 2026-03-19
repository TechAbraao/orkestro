from flask import Blueprint, render_template, request, redirect, url_for, g
from source.app.utils.decorators.authorizations import authenticated, api_permissions
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

