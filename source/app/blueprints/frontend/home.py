from flask import Blueprint, render_template, request, redirect, url_for
from source.app.utils.decorators.authorizations import authorized_client, authorization_required

from source.app.blueprints.routes import vws

@vws.get("/")
@authorized_client
def views_root():
    return redirect(url_for("vws.views_homepage"))

@vws.get("/home")
@authorized_client
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
@authorized_client
def views_login():
    rendering_strategy = {
        "url": f"{request.path}",
        "profile": {
            "roles": f""
        },
        "logged": False
    }

    return render_template("pages/signin.jinja2", strategy=rendering_strategy)

@vws.get("/signup")
@authorization_required()
def views_register():
    rendering_strategy = {
        "url": f"{request.path}",
        "profile": {
            "roles": f""
        },
        "logged": False
    }

    return render_template("pages/signup.jinja2", strategy=rendering_strategy)

