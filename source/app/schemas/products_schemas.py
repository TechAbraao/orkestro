from source.app.settings.definitions_settings import ma
from marshmallow import validate, fields
from marshmallow.validate import URL


class ProductsSchema(ma.Schema):
    name = fields.String(required=True, validate=validate.Length(min=6, max=255))
    description = fields.String(required=True, allow_none=True)
    price = fields.Float(required=True)


class ProductUpdateSchema(ma.Schema):
    """ Schema for updating existing product. """

    id = fields.UUID(required=True)
    name = fields.String(required=True, validate=validate.Length(min=6, max=255))
    description = fields.String(required=True, allow_none=True)
    price = fields.Float(required=True)
