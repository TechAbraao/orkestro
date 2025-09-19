from flask import Blueprint, jsonify, request
from source.app.utils.decorators.authorizations import authorization_required
from source.app.settings.logging_settings import get_logger

logger = get_logger(__name__)
about_auth = Blueprint("about_auth", __name__, url_prefix="/api/stores")


@about_auth.route("/me", methods=["GET"])
@authorization_required
def about_me():
    token = request.cookies.get("access_token")
    logger.info(f"Your about me token is '{token}'")

    return jsonify({
        "message": "User info retrieved successfully",
        "success": True
    })
