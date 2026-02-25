from source.app.settings.definitions_settings import ma
from marshmallow import validate

class MenuSchema(ma.Schema):
    name = ma.String(required=True, validate=validate.Length(min=6, max=30))
    description = ma.String(required=True)
    roles = ma.String(required=True)

class UUIDSchema(ma.Schema):
    id = ma.UUID(required=True)

class MenuStatus(ma.Schema):
    status = ma.String(required=True)