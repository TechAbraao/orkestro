from source.app.settings.definitions_settings import db as database

menu_product = database.Table(
    "menu_product",
    database.Column("menu_id", database.UUID(as_uuid=True), database.ForeignKey("menus.id"), primary_key=True),
    database.Column("product_id", database.UUID(as_uuid=True), database.ForeignKey("products.id"), primary_key=True),
)