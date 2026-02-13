from flask import render_template, request, abort, redirect, url_for, g
from source.app.utils.decorators.authorizations import permissions
from source.app.services import stores_services
from source.app.blueprints.routes import vws

""" Páginas para diferentes tipos de Estatísticas """
""" 
    1. Histórico de Pedidos
    2. Histórico de Clientes
"""
@vws.route("/historic")
@permissions(strategy="jwt", roles=["USER", "ADMIN"])
def vws_historic():
    redirect_uri = url_for("vws.views_main_dashboard")
    tab = request.args.get("tab")
    if tab == "orders":
        store_id = g.jwt_claims.get("sub")
        menu_id = stores_services.get_menu_by_store_id(store_id)

        strategy = {
            "profile": {
                "menu_id": menu_id
            }
        }
        return render_template("/pages/historic_orders.jinja2", strategy=strategy)
    elif tab == "customers":
        # TODO: Futura implementação do histórico de clientes

        strategy = {
            "profile": {

            }
        }
        return render_template("/pages/historic_customers.jinja2", strategy=strategy)
    elif not tab:
        return redirect(redirect_uri)
    return redirect(redirect_uri)