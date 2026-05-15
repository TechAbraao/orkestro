from source.app.settings.definitions_settings import ma
from marshmallow import fields, validate


class ReviewsSchema(ma.Schema):
    note = fields.Int(required=True)
    category = fields.List(fields.String, required=True)
    description = fields.String( required=False)
    to = fields.String(required=True)
    by = fields.String(required=True)
