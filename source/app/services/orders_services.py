from source.app.repository.orders_repository import OrdersRepository
from source.app.utils.decorators.database import database_connection
from source.app.entities.orders_entity import OrderEntity

from uuid import uuid4

class OrdersServices:
    def __init__(self):
        self.orders_repository = OrdersRepository()

    @database_connection
    def save_order_the_menu(self, data):
        order = OrderEntity(
            id=str(uuid4()),
            status=data.get("status", "done"),
            user_id=data.get("user_id", None),
            menu_id=data.get("menu_id", None),
            total_value=data.get("total_value", None),
            telephone=data.get("telephone"),
            name=data.get("name")
        )
        saved = self.orders_repository.create_order(order)
        if not saved:
            return False
        return True

    @database_connection
    def get_order_by_menu_id(self, menu_id):
        orders = self.orders_repository.get_order_by_menu_id(menu_id)
        if not orders:
            return []
        return [order.serialize for order in orders]

    @database_connection
    def delete_order_by_id(self, order_id):
        deleted = self.orders_repository.delete_by_order_id(order_id)
        if not deleted:
            return False
        return True

    @database_connection
    def update_order_status(self, status, order_id):
        updated = self.orders_repository.update_status_by_order_id(status, order_id)
        if not updated:
            return None
        return updated.serialize

    @database_connection
    def count_orders_done(self, menu_id, status="done"):
        return self.orders_repository.count_orders_by_status(menu_id=menu_id, status=status)