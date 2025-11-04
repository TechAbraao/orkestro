from source.app.settings.definitions_settings import ma

class CustomersSchema(ma.Schema):
    name = ma.String(required=True)
    telephone = ma.String(required=True)
    address = ma.String(required=True)
    number = ma.Integer(required=True)