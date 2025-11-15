from flask import render_template, request, abort, redirect, url_for
from source.app.blueprints.routes import vws

""" Páginas para diferentes tipos de Estatísticas """
""" 
    1. Relatórios Gráficos
    2. Histórico de Pedidos
    3. Histórico de Clientes
"""
@vws.route("/statistics")
def vws_statistics():
    redirect_uri = url_for("main_frontend.views_main_dashboard")
    tab = request.args.get("tab")
    if tab == "reports":
        return "<h1>Relatórios</h1>"
    elif tab == "orders":
        return "<h1>Histórico de Pedidos</h1>"
    elif tab == "customers":
        return "<h1>Histórico de Clientes</h1>"
    elif not tab:
        return redirect(redirect_uri)
    return redirect(redirect_uri)