from source.app.services.menu_services import MenuServices
from source.app.services.categories_services import CategoriesServices
from source.app.services.products_services import ProductsServices
from source.app.services.stores_services import StoresServices
from source.app.services.authorizations_services import AuthorizationsServices
from source.app.services.opening_hours_services import OpeningHoursServices
from source.app.services.customers_services import CustomersServices
from source.app.services.orders_services import OrdersServices
from source.app.services.analysis_services import AnalysisServices

# Initialize service instances
menu_services = MenuServices()
categories_services = CategoriesServices()
products_services = ProductsServices()
stores_services = StoresServices()
authorizations_services = AuthorizationsServices()
opening_hours_services = OpeningHoursServices()
customers_services = CustomersServices()
orders_services = OrdersServices()
analysis_services = AnalysisServices()