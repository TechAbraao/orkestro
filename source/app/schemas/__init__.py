from source.app.schemas.menu_schemas import *
from source.app.schemas.categories_schemas import *
from source.app.schemas.products_schemas import *
from source.app.schemas.stores_schemas import *
from source.app.schemas.opening_hours_schemas import *
from source.app.schemas.orders_schemas import *
from source.app.schemas.customers_schemas import *
from source.app.schemas.reviews_schemas import *

# Initialize schema instances
menu_schema = MenuSchema()
uuid_schema = UUIDSchema()
categories_schema = CategoriesSchema()
products_schemas = ProductsSchema()
stores_schemas = StoresSchema()
login_stores_schemas = LoginStoresSchema()
menu_status = MenuStatus()
opening_hours_schemas = OpeningHoursSchema()
orders_schemas = OrdersSchema()
customers_schemas = CustomersSchema()
reviews_schemas = ReviewsSchema()