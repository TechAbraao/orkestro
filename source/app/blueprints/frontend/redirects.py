from flask import redirect, url_for
from source.app.utils.decorators.authorizations import authenticated
from source.app.blueprints.routes import vws

@vws.route("/redirect-by-role")
@authenticated
def redirect_by_role():
    return redirect(url_for("vws.views_login"))
