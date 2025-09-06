from source.app.settings.definitions_settings import db as database

from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import uuid


class CategoriesEntity(database.Model):
    __tablename__ = "categories"

    id = database.Column(database.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = database.Column(database.String, nullable=False)
    description = database.Column(database.String, nullable=True)
    url_image = database.Column(database.String(255), nullable=True)
    created_at = database.Column(
        database.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    menu_id = database.Column(
        database.UUID(as_uuid=True), database.ForeignKey("menus.id", ondelete="CASCADE"), nullable=False
    )

    menu = database.relationship("MenusEntity", back_populates="categories")
    products = database.relationship("ProductsEntity", back_populates="category", cascade="all, delete")

    @property
    def serialize(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "menu_id": str(self.menu_id),
            "url_image": self.url_image,
            "products": [product.serialize for product in self.products]
        }
