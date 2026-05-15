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
       pass
    elif not tab:
        return redirect(redirect_uri)
    return redirect(redirect_uri)
