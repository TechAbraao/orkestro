from functools import wraps
from flask import request, redirect, url_for, abort, jsonify
from source.app.utils.jwt import decrypt_token
from source.app.settings.application_settings import application_settings as credentials
import base64
from flask import g

def get_token_from_request():
    token = request.cookies.get("access_token")
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

    return token

def redirect_by_role_logic(roles):

    role_redirect_map = {
        "ADMIN": "vws.views_main_dashboard",
        "PRIVILEGED": "vws.views_profile_dashboard",
        "COMMON": "vws.views_orders_dashboard"
    }

    for role in roles:
        if role in role_redirect_map:
            return redirect(url_for(role_redirect_map[role]))

    return redirect(url_for("vws.views_login"))

def permissions(strategy="jwt", roles=None):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):

            claims = None

            ## Utilizou um Token JWT? ##
            ## 1. Cenário: Token JWT Strategy ##
            if strategy in ("jwt", "either"):
                token = get_token_from_request()
                if token:
                    try:
                        claims = decrypt_token(token)
                    except ValueError:
                        pass

                if strategy == "jwt" and not claims:
                    return redirect(url_for("vws.views_login"))

            ## Utilizou um Basic Authorization? ##
            ##  2. Cenário: Basic Authorization Strategy
            if strategy in ("basic", "either") and not claims:
                auth_header = request.headers.get("Authorization")

                if auth_header and auth_header.startswith("Basic "):
                    try:
                        base64_credentials = auth_header.split(" ")[1]
                        decoded = base64.b64decode(base64_credentials).decode("utf-8")
                        email, password = decoded.split(":", 1)

                        if (
                            credentials.ADMIN_EMAIL == email
                            and credentials.ADMIN_PASSWORD == password
                        ):
                            claims = {
                                "roles": ["ADMIN"]
                            }

                    except Exception:
                        pass

                if strategy == "basic" and not claims:
                    return (
                        jsonify({"message": "Unauthorized"}),
                        401,
                        {"WWW-Authenticate": "Basic realm='Login required'"}
                    )

            ## Não se autenticou? ##
            ## 3. Cenário: Caso não tenha se autenticado ##
            if not claims:
                abort(401)

            g.jwt_claims = claims

            ## Verifica se o usuário possui pelo menos uma das roles exigidas para acessar o recurso. ##
            ## 4. Cenário: Autorização baseada em roles (RBAC) ##
            if roles:
                user_roles = claims.get("roles", [])

                # 5. Cenário: Lógica que verifica as permissões necessárias
                if not any(role in user_roles for role in roles):

                    ## 6. Sem permissões através da /api
                    if request.path.startswith("/api"):
                        abort(403, "Acesso negado: Você não possui permissão para acessar este recurso.")

                    ## 7. Sem permissões através da /web
                    return redirect(url_for("vws.redirect_by_role"))

            return f(*args, **kwargs)
        return decorated
    return decorator

def authenticated(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_from_request()
        if token:
            try:
                claims = decrypt_token(token)
                roles = claims.get("roles", [])

                return redirect_by_role_logic(roles)
            except ValueError:
                pass
        return f(*args, **kwargs)
    return decorated

