from flask import Blueprint
from source.app.utils.responses import Response

sign_in_auth = Blueprint("sign_in_auth", __name__, url_prefix="/api/auth")

""" 1. Enter the platform """
@sign_in_auth.route("/signin")
def enter_the_plataform():
    pass