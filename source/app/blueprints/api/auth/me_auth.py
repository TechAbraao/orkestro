from flask import Blueprint, jsonify, request
from source.app.utils.decorators.authorizations import permissions
from source.app.settings.logging_settings import get_logger
from source.app.services import stores_services
from source.app.utils.responses import Response
from source.app.utils.jwt import *

logger = get_logger(__name__)
about_auth = Blueprint("about_auth", __name__, url_prefix="/api/stores")

@about_auth.route("/me", methods=["GET"])
@permissions(roles=["USER", "ADMIN"])
def about_me_store():
    token = request.cookies.get("access_token")
    logger.info(f"Your about me token is '{token}'")

    decrypt = decrypt_token(token)
    logger.info(f"Decrypted token: '{decrypt}'")

    store_me = stores_services.about_me_store_account(decrypt["sub"])

    return Response.success(
        message="User info retrieved successfully",
        status_code=200,
        data=store_me
    )
