from source.app.settings.definitions_settings import ma
from marshmallow import fields, validate

class StoresSchema(ma.Schema):
    name = fields.String(required=True, validate=validate.Length(min=6, max=30))
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6, max=15))
    telephone = fields.String(required=True, validate=validate.Length(equal=9))

class LoginStoresSchema(ma.Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6, max=15))