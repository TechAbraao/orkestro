from source.app.settings.definitions_settings import db as database
import uuid
import datetime

class MenuProductsEntity(database.Model):
    __tablename__ = "menu_product"
    id = database.Column(database.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    menu_id = database.Column(database.UUID(as_uuid=True), database.ForeignKey("menu.id"))
    product_id = database.Column(database.UUID(as_uuid=True), database.ForeignKey("product.id"))
