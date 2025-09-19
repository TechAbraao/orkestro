from flask import Blueprint, render_template
from source.app.utils.decorators.authorizations import authorization_required

main_frontend = Blueprint("main_frontend", __name__, url_prefix="")


@main_frontend.get("/dashboard")
@authorization_required
def views_main_dashboard():
    return render_template("pages/dashboard.jinja2")


@main_frontend.get("/profile")
@authorization_required
def views_profile_dashboard():
    return render_template("pages/store_profile.jinja2")
