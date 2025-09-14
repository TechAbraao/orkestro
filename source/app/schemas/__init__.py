from source.app.schemas.menu_schemas import *
from source.app.schemas.categories_schemas import *
from source.app.schemas.products_schemas import *
from source.app.schemas.stores_schemas import *

# Initialize schema instances
menu_schema = MenuSchema()
uuid_schema = UUIDSchema()
categories_schema = CategoriesSchema()
products_schemas = ProductsSchema()
stores_schemas = StoresSchema()