from source.app.settings.definitions_settings import db as database
import uuid
from datetime import datetime, timezone

class OrderEntity(database.Model):
    __tablename__ = "orders"

    id = database.Column(database.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = database.Column(database.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    total = database.Column(database.Numeric, nullable=False)
    user_id = database.Column(database.UUID(as_uuid=True), database.ForeignKey("users.id"))

from source.app.entities.users_entity import UsersEntity
from source.app.entities.orders_products_entity import OrderProductsEntity

OrderEntity.user = database.relationship(
    UsersEntity,
    back_populates="orders"
)
OrderEntity.order_products = database.relationship(
    OrderProductsEntity,
    back_populates="order"
)
