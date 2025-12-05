from flask import render_template, request, abort, redirect, url_for
from source.app.blueprints.routes import vws

""" Páginas para diferentes tipos de Integrações """
""" 
    1. Integração: WhatsApp 
    2. Integração: ...
    3. Integração: ...
    n. Integrações: ...
"""
@vws.route("/integrations")
def vws_integrations():
    redirect_uri = url_for("vws.views_main_dashboard")
    tab = request.args.get("tab")
    if tab == "whatsapp":
        return render_template("/pages/integration_whatsapp.jinja2")
    elif not tab:
        return redirect(redirect_uri)
    return redirect(redirect_uri)