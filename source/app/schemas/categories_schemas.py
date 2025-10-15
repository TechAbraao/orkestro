from source.app.settings.definitions_settings import ma
from marshmallow import validate, fields
from marshmallow.validate import URL

class CategoriesSchema(ma.Schema):
    name = ma.String(required=True, validate=validate.Length(min=3, max=30))
    description = ma.String(required=True)
    url_image = fields.String(required=False, validate=[URL(), validate.Length(max=255)])
