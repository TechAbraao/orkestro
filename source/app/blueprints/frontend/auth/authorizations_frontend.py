from flask import Blueprint, request, render_template

authorizations_frontend = Blueprint("authorizations_frontend", __name__, url_prefix="")

@authorizations_frontend.get("/signin")
def views_login():
    return render_template("pages/signin.jinja2")

@authorizations_frontend.get("/signup")
def views_register():
    return render_template("pages/signup.jinja2")