from source.app.settings.definitions_settings import ma
from marshmallow import validate

class ProductItemSchema(ma.Schema):
    product_id = ma.UUID(required=True)
    quantity = ma.Integer(required=True)

class OrdersSchema(ma.Schema):
    user_id = ma.UUID(required=True)
    menu_id = ma.UUID(required=True)
    products = ma.List(
        ma.Nested(ProductItemSchema),
        required=True,
        validate=validate.Length(min=1)
    )

class OrdersStatus(ma.Schema): pass