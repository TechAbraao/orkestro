from functools import wraps
from flask import request, redirect, url_for
from source.app.utils.jwt import decrypt_token
from flask import g

def authorization_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get("access_token")
        if not token:
            return redirect(url_for("authorizations_frontend.views_login"))
        try:
            claims = decrypt_token(token)
        except ValueError:
            return redirect(url_for("authorizations_frontend.views_login"))

        g.jwt_claims = claims
        return f(*args, **kwargs)

    return decorated


def authorized_client(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get("access_token")
        if token:
            try:
                decrypt_token(token)
                return redirect(url_for("main_frontend.views_main_dashboard"))
            except ValueError:
                pass
        return f(*args, **kwargs)
    return decorated
