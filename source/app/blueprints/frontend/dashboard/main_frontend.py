from flask import Blueprint, render_template

main_frontend = Blueprint("main_frontend", __name__, url_prefix="")

# To access this feature, you will need to be authenticated.
@main_frontend.get("/dashboard")
def views_main_dashboard():
    return render_template("pages/dashboard.jinja2")