from flask import request, jsonify, abort, g
from source.app.blueprints.routes import api
from source.app.services import stores_services
from source.app.settings.logging_settings import get_logger
from source.app.utils.decorators.authorizations import authenticated, api_permissions
from source.app.schemas import reviews_schemas
from source.app.services import reviews_services

logger = get_logger(__name__)
dir_name = "reviews.py"

@api.route("/reviews", methods=["GET"])
def get_all_reviews():
    all_reviews = reviews_services.all_reviews()
    return jsonify({
        "data": all_reviews,
        "statusCode": 200
    }), 200

@api.route("/reviews/me", methods=["GET"])
@api_permissions(strategy="jwt", roles=["ADMIN", "PRIVILEGED"])
def get_my_all_reviews():
    store_id = g.jwt_claims.get("sub")
    # roles = g.jwt_claims.get("roles")

    current_user = stores_services.get_store_by_id(store_id)
    comments_sent = reviews_services.all_reviews_to(current_user.get("name", None))
    comments_sent_serialize = [comments.serialize for comments in comments_sent]

    return jsonify({
        "data": comments_sent_serialize
        })

@api.route("/reviews", methods=["POST"])
def post_review():
    body = request.get_json()
    validate_body = reviews_schemas.load(body)
    review_added = reviews_services.add_review(body)
    return jsonify({
        "msg": f"saved: {review_added}"
    })
