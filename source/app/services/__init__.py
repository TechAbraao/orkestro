from source.app.services.menu_services import MenuServices
from source.app.services.categories_services import CategoriesServices
from source.app.services.products_services import ProductsServices
from source.app.services.stores_services import StoresServices
from source.app.services.authorizations_services import AuthorizationsServices

# Initialize service instances
menu_services = MenuServices()
categories_services = CategoriesServices()
products_services = ProductsServices()
stores_services = StoresServices()
authorizations_services = AuthorizationsServices()