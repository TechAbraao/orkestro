from source.app.settings.definitions_settings import db as database

from uuid import uuid4

class StoreEntity(database.Model):
    __tablename__ = "stores"

    id = database.Column(database.UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = database.Column(database.String, nullable=False)