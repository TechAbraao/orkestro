from flask import Blueprint, jsonify
from source.app.utils.decorators.authorizations import authorization_required

analytics_dashboard = Blueprint("analytics_dashboard", __name__, url_prefix="/api")

@analytics_dashboard.route("/analytics")
@authorization_required
def get_analytics():
    return jsonify({"message": "OK"})