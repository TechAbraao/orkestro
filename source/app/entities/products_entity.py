from decimal import Decimal
from typing import Dict, Any
from source.app.settings.definitions_settings import db as database
from datetime import datetime, timezone
import uuid


class ProductsEntity(database.Model):
    __tablename__ = "products"

    id = database.Column(database.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = database.Column(database.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    name = database.Column(database.String, nullable=False)
    description = database.Column(database.Text, nullable=True)
    price = database.Column(database.Numeric, nullable=False)
    category_id = database.Column(database.UUID(as_uuid=True), database.ForeignKey("categories.id"))
    image_url = database.Column(database.String(255), nullable=True)
    activated = database.Column(
        database.Boolean,
        default=True
    )

    category = database.relationship("CategoriesEntity", back_populates="products")

    @property
    def serialize(self) -> Dict[str, Any]:
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "price": float(self.price) if isinstance(self.price, Decimal) else self.price,
            "image_url": self.image_url,
            "category_id": str(self.category_id) if self.category_id else None,
            "activated": bool(self.activated),
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

from source.app.entities.associations_tables_entity import menu_product
from source.app.entities.menus_entity import MenusEntity
from source.app.entities.orders_products_entity import OrderProductsEntity

ProductsEntity.menus = database.relationship(
    MenusEntity, secondary=menu_product, back_populates="products"
)

ProductsEntity.order_products = database.relationship(
    OrderProductsEntity, back_populates="product"
)
