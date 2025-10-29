from source.app.settings.definitions_settings import db as database
from datetime import datetime, timezone
import uuid

class OrderProductsEntity(database.Model):
    __tablename__ = "order_products"

    id = database.Column(database.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = database.Column(database.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    order_id = database.Column(database.UUID(as_uuid=True), database.ForeignKey("orders.id"))
    product_id = database.Column(database.UUID(as_uuid=True), database.ForeignKey("products.id"))
    quantity = database.Column(database.Integer, nullable=False)
    price = database.Column(database.Numeric, nullable=False)

from source.app.entities.orders_entity import OrderEntity
from source.app.entities.products_entity import ProductsEntity

OrderProductsEntity.order = database.relationship(OrderEntity, back_populates="order_products")
OrderProductsEntity.product = database.relationship(ProductsEntity, back_populates="order_products")
