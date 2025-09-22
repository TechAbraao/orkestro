from source.app.settings.definitions_settings import db as database
from datetime import datetime, timezone
from source.app.entities.stores_entity import StoresEntity
import uuid

class MenusEntity(database.Model):
    __tablename__ = "menus"

    id = database.Column(database.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = database.Column(
        database.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    name = database.Column(database.String, nullable=False)
    slug = database.Column(database.String, nullable=True)
    description = database.Column(database.Text, nullable=True)
    activated = database.Column(
        database.Boolean,
        nullable=False,
        default=False
    )
    categories = database.relationship(
        "CategoriesEntity", back_populates="menu", cascade="all, delete"
    )
    store_id = database.Column(
        database.UUID(as_uuid=True),
        database.ForeignKey("stores.id", ondelete="CASCADE"),
        nullable=False
    )
    store = database.relationship("StoresEntity", back_populates="menus")


    @property
    def serialize(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "slug": self.slug
            # "categories": [category.serialize for category in self.categories] if self.categories else [],
            # "products": [product.serialize for product in self.products] if self.products else []
        }

    def serialize_client(self, include_categories: bool = True, include_products: bool = True):
        data = {
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "slug": self.slug,
        }

        if include_categories:
            data["categories"] = [
                category._serialize(include_products=include_products) for category in self.categories
            ]

        if include_products:
            data["products"] = [product.serialize for product in self.products] if self.products else []

        return data


from source.app.entities.associations_tables_entity import menu_product
from source.app.entities.products_entity import ProductsEntity

MenusEntity.products = database.relationship(
    ProductsEntity, secondary=menu_product, back_populates="menus"
)
