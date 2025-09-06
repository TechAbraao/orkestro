from functools import wraps
from flask import request, jsonify
from marshmallow import Schema, ValidationError


def validate_request(schema: Schema):
    """
    Decorator that validates request body + path/query params
    against a Marshmallow schema.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                payload = {**(request.get_json(silent=True) or {}), **request.args, **kwargs}
                data = schema.load(payload)
            except ValidationError as err:
                return jsonify({
                    "success": False,
                    "errors": err.messages
                }), 400
            return func(data, *args, **kwargs)
        return wrapper
    return decorator
