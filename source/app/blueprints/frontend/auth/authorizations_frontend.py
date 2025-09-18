from flask import Blueprint, render_template, request

authorizations_frontend = Blueprint("authorizations_frontend", __name__, url_prefix="")

@authorizations_frontend.get("/signin")
def views_login():
    rendering_strategy = {
        "url": f"{request.path}",
        "profile": {
            "roles": f""
        },
        "logged": False
    }

    return render_template("pages/signin.jinja2", strategy=rendering_strategy)

@authorizations_frontend.get("/signup")
def views_register():
    rendering_strategy = {
        "url": f"{request.path}",
        "profile": {
            "roles": f""
        },
        "logged": False
    }

    return render_template("pages/signup.jinja2", strategy=rendering_strategy)