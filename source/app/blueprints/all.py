""" All routes should be imported here. """

""" API Layer Routes. """
from source.app.blueprints.api.admin.categories_admin import categories_bp
from source.app.blueprints.api.admin.menus_admin import menus_bp
from source.app.blueprints.api.admin.products_admin import products_bp
from source.app.blueprints.api.client.menus_client import menus_client
from source.app.blueprints.api.client.orders_client import orders_client
from source.app.blueprints.api.auth.sign_up_auth import sign_up_auth
from source.app.blueprints.api.auth.sign_in_auth import sign_in_auth
from source.app.blueprints.api.dashboard.analytics_dashboard import analytics_dashboard
from source.app.blueprints.api.auth.me_auth import about_auth
from source.app.blueprints.api.client.customers import customers

""" Front-end Routes. """
from source.app.blueprints.frontend.auth.authorizations_frontend import *
from source.app.blueprints.frontend.dashboard.main_frontend import *
from source.app.blueprints.frontend.home.homepage_frontend import *
from source.app.blueprints.frontend.client.menus_client_frontend import *
