from source.app.settings.definitions_settings import db as database
import uuid
from datetime import datetime, timezone

class UsersEntity(database.Model):
    __tablename__ = "users"

    id = database.Column(database.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = database.Column(database.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    telephone = database.Column(database.String, nullable=True, unique=True)
    address = database.Column(database.String, nullable=True)
    name = database.Column(database.String, nullable=False)
    house_number = database.Column(database.Integer, nullable=False)

    @property
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "telephone": self.telephone,
            "address": self.address,
            "house_number": self.house_number,
            "created_at": self.created_at
        }

from source.app.entities.orders_entity import OrderEntity

UsersEntity.orders = database.relationship(
    OrderEntity,
    back_populates="user",
    cascade="all, delete-orphan"
)
