from source.app.settings.definitions_settings import ma
from marshmallow import fields, validates, ValidationError
import datetime

class OpeningHoursSchema(ma.Schema):
    day = fields.String(required=True)
    open = fields.Time(required=True, format="%H:%M")
    close = fields.Time(required=True, format="%H:%M")
