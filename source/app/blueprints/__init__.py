""" All routes should be imported here. """

""" Admin Routes. """
from source.app.blueprints.api.admin.categories_admin import categories_bp
from source.app.blueprints.api.admin.menus_admin import menus_bp
from source.app.blueprints.api.admin.products_admin import products_bp

""" Clients Routes. """
from source.app.blueprints.api.client.menus_client import menus_client
from source.app.blueprints.api.client.orders_client import orders_client

""" Dashboard Routes. """


""" Auth Routes. """
from source.app.blueprints.api.auth.sign_up_auth import sign_up_auth


