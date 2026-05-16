from flask import request, jsonify
from source.app.blueprints.routes import api
from source.app.settings.logging_settings import get_logger
from source.app.schemas import reviews_schemas
from source.app.services import reviews_services

logger = get_logger(__name__)
dir_name = "reviews.py"


@api.route("/reviews", methods=["GET"])
def get_all_reviews():
    
    
    return jsonify({
        "data": ""
    }), 200

@api.route("/reviews", methods=["POST"])
def post_review():
    body = request.get_json()
    validate_body = reviews_schemas.load(body)
    review_added = reviews_services.add_review(body)
    return jsonify({
        "msg": f"saved: {review_added}"
    })