from flask import Blueprint, render_template, request, redirect, url_for

homepage_frontend = Blueprint("homepage_frontend", __name__, url_prefix="")

@homepage_frontend.get("/")
def views_root():
    return redirect(url_for("homepage_frontend.views_homepage"))

@homepage_frontend.get("/home")
def views_homepage():
    rendering_strategy = {
        "url": f"{request.path}",
        "profile": {
            "roles": f""
        },
        "logged": False
    }
    return render_template("/pages/homepage.jinja2", strategy=rendering_strategy)
