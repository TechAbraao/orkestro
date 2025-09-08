""" All routes should be imported here. """

""" Routes for the administrator to manipulate. """

""" Admin Routes """
from source.app.blueprints.api.admin.categories_admin import categories_bp
from source.app.blueprints.api.admin.menus_admin import menus_bp
from source.app.blueprints.api.admin.products_admin import products_bp

""" Clients Routes """
from source.app.blueprints.api.client.menus_client import menus_client
from source.app.blueprints.api.client.orders_client import orders_client

""" Dashboard Routes """
