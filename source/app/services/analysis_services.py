from source.app.repository.orders_repository import OrdersRepository
from source.app.repository.menus_repository import MenusRepository
from source.app.utils.decorators.database import database_connection

class AnalysisServices:
    def __init__(self):
        self.orders_repository = OrdersRepository()
        self.menus_repository = MenusRepository()

    @database_connection
    def number_or_orders_placed(self, menu_id):
        value = self.orders_repository.number_of_orders_placed(menu_id)
        return value

    @database_connection
    def total_sales_last_24h(self, menu_id):
        return self.orders_repository.get_total_sales_last_24h(menu_id)