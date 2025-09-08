from flask import Blueprint

orders_client = Blueprint(
    "orders_client",
    __name__,
    url_prefix=""
)

