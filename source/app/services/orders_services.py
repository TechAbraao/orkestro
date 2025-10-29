from source.app.repository.orders_repository import OrdersRepository
from source.app.utils.decorators.database import database_connection

class OrdersServices:
    def __init__(self):
        self.orders_repository = OrdersRepository()

    @database_connection
    def new_order_the_menu(self, menu_id, data):
        pass