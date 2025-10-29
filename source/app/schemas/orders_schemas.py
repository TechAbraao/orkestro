from source.app.settings.definitions_settings import ma

class OrdersSchema(ma.Schema):
    user_id = None
    menu_id = None
    products = None