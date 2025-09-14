from flask import Blueprint, request, jsonify
from source.app.utils.responses import Response
from source.app.schemas import stores_schemas

sign_up_auth = Blueprint(
    "sign_up_auth",
    __name__,
    url_prefix="/api/auth"
)

""" 1. Create a new account - Store """
@sign_up_auth.route("/signup", methods=["POST"])
def create_new_account():
    body = request.get_json()
    body_validated = stores_schemas.load(body)

    return Response.success(
        message="Store created successfully.",
        status_code=200,
        data=body_validated
    )
