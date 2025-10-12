from flask import Blueprint, render_template, request
from source.app.utils.decorators.authorizations import authorized_client

authorizations_frontend = Blueprint("authorizations_frontend", __name__, url_prefix="")

@authorizations_frontend.get("/signin")
@authorized_client
def views_login():
    rendering_strategy = {
        "url": f"{request.path}",
        "profile": {
            "roles": f""
        },
        "logged": False
    }

    return render_template("pages/auth/signin.jinja2", strategy=rendering_strategy)

@authorizations_frontend.get("/signup")
@authorized_client
def views_register():
    rendering_strategy = {
        "url": f"{request.path}",
        "profile": {
            "roles": f""
        },
        "logged": False
    }

    return render_template("pages/auth/signup.jinja2", strategy=rendering_strategy)

