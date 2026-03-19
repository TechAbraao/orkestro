from flask import render_template, request, abort, redirect, url_for, g
from source.app.blueprints.routes import vws
from source.app.utils.decorators.authorizations import api_permissions
from source.app.services import stores_services


""" Páginas para diferentes tipos de Configurações"""
@vws.route("/settings")
@api_permissions(strategy="jwt", roles=["ADMIN", "PRIVILEGED"])
def vws_settings():
    redirect_uri = url_for("vws.views_main_dashboard")
    tab = request.args.get("tab")
    if tab == "whatsapp":
        return render_template("/pages/integration_whatsapp.jinja2")
    elif tab == "blocked":
        return render_template("/pages/blocked_phones.jinja2")
    elif tab == "stores":
        store_id = g.jwt_claims.get("sub")
        roles = g.jwt_claims.get("roles")
        menu_id = stores_services.get_menu_by_store_id(store_id)

        rendering_strategy = {
            "url": f"{request.path}",
            "profile": {
                "roles": roles,
                "menu_id": menu_id.get("id"),
            },
            "logged": False,
        }
        return render_template("pages/store_manager.jinja2", strategy=rendering_strategy)
    elif not tab:
        return redirect(redirect_uri)
    return redirect(redirect_uri)
