from source.app.settings.definitions_settings import db as database
from source.app.entities.menus_entity import MenusEntity
import uuid
from datetime import datetime, timezone

class OrderEntity(database.Model):
    __tablename__ = "orders"

    id = database.Column(database.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = database.Column(database.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    total_value = database.Column(database.Numeric, nullable=False)
    status = database.Column(database.String(20), nullable=False)
    user_id = database.Column(database.UUID(as_uuid=True), database.ForeignKey("users.id"))
    menu_id = database.Column(database.UUID(as_uuid=True),database.ForeignKey("menus.id", ondelete="CASCADE"),nullable=False)

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

OrderEntity.menu = database.relationship(
    MenusEntity,
    back_populates="orders"
)
