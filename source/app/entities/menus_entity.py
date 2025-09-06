from source.app.settings.definitions_settings import db as database
from datetime import datetime, timezone
import uuid

class MenusEntity(database.Model):
    __tablename__ = "menus"

    id = database.Column(database.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = database.Column(
        database.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    name = database.Column(database.String, nullable=False)
    description = database.Column(database.Text, nullable=True)

    categories = database.relationship(
        "CategoriesEntity", back_populates="menu", cascade="all, delete"
    )
    @property
    def serialize(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            # "categories": [category.serialize for category in self.categories] if self.categories else [],
            # "products": [product.serialize for product in self.products] if self.products else []
        }


from source.app.entities.associations_tables_entity import menu_product
from source.app.entities.products_entity import ProductsEntity

MenusEntity.products = database.relationship(
    ProductsEntity, secondary=menu_product, back_populates="menus"
)
