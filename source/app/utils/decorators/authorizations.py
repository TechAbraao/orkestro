from functools import wraps
from flask import request, redirect, url_for, abort
from source.app.utils.jwt import decrypt_token
from flask import g

def permissions(roles=None):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.cookies.get("access_token")

            # Caso não tenha o Token, verifica Authorization Bearer
            if not token:
                auth_header = request.headers.get("Authorization")
                if auth_header and auth_header.startswith("Bearer "):
                    token = auth_header.split(" ")[1]

            if not token:
                return redirect(url_for("vws.views_login"))

            # Descriptografia do JWT
            try:
                claims = decrypt_token(token)
            except ValueError:
                return redirect(url_for("vws.views_login"))

            g.jwt_claims = claims
            user_roles = claims.get("roles", [])

            # Só valida roles se foi passado algo
            if roles:
                if not any(role in user_roles for role in roles):
                    abort(403)

            return f(*args, **kwargs)

        return decorated
    return decorator

def authorized_client(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get("access_token")
        if token:
            try:
                decrypt_token(token)
                return redirect(url_for("vws.views_main_dashboard"))
            except ValueError:
                pass
        return f(*args, **kwargs)
    return decorated

def cart_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        cart = None
