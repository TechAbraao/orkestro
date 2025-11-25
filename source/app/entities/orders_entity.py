from source.app.settings.definitions_settings import db as database
from sqlalchemy import Sequence
from source.app.entities.menus_entity import MenusEntity
import uuid
from datetime import datetime, timezone

class OrderEntity(database.Model):
    __tablename__ = "orders"

    __table_args__ = (
        database.UniqueConstraint("menu_id", "order_number", name="uq_menu_order_number"),
    )

    id = database.Column(database.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = database.Column(database.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    total_value = database.Column(database.Numeric, nullable=False)
    status = database.Column(database.String(20), nullable=False)
    user_id = database.Column(
        database.UUID(as_uuid=True),
        database.ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )
    menu_id = database.Column(database.UUID(as_uuid=True),database.ForeignKey("menus.id", ondelete="CASCADE"),nullable=False)
    name = database.Column(database.String(), nullable=False)
    telephone = database.Column(database.String(), nullable=False)
    order_number = database.Column(database.Integer, nullable=False)

    @property
    def serialize(self):
        return {
            "id": str(self.id),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "total_value": float(self.total_value),
            "status": self.status,
            "user_id": str(self.user_id) if self.user_id else None,
            "menu_id": str(self.menu_id) if self.menu_id else None,
            "name": str(self.name),
            "telephone": str(self.telephone),
            "order_number": int(self.order_number)
        }
from source.app.entities.users_entity import UsersEntity
from source.app.entities.orders_products_entity import OrderProductsEntity

OrderEntity.user = database.relationship(
    UsersEntity,
    back_populates="orders"
)
OrderEntity.order_products = database.relationship(
    OrderProductsEntity,
    back_populates="order",
    cascade="all, delete-orphan",
    passive_deletes=True
)

OrderEntity.menu = database.relationship(
    MenusEntity,
    back_populates="orders"
)
