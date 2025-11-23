from source.app.repository.orders_repository import OrdersRepository
from source.app.repository.orders_products_repository import OrdersProductsRepository
from source.app.utils.decorators.database import database_connection
from source.app.entities.orders_entity import OrderEntity
from datetime import datetime, timedelta

from uuid import uuid4

class OrdersServices:
    def __init__(self):
        self.orders_repository = OrdersRepository()
        self.orders_products_repository = OrdersProductsRepository()

    @database_connection
    def save_order_the_menu(self, data):
        new_order_number = self.orders_repository.next_order_number(data["menu_id"])
        order = OrderEntity(
            id=str(uuid4()),
            status=data.get("status", "done"),
            user_id=data.get("user_id", None),
            menu_id=data.get("menu_id", None),
            total_value=data.get("total_value", None),
            telephone=data.get("telephone"),
            name=data.get("name"),
            order_number=new_order_number
        )
        saved = self.orders_repository.create_order(order)
        if not saved:
            return False
        return True, str(order.id)

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

    @database_connection
    def save_products_in_order(self, order_id, products):
        """
        Salva uma lista de produtos para um pedido específico.
        - order_id: ID do pedido recém-criado.
        - products: lista de produtos, cada item contendo product_id, quantity e price.
        """
        if not order_id:
            raise ValueError("order_id é obrigatório")
        if not products or not isinstance(products, list):
            raise ValueError("A lista de produtos não pode ser vazia")

        products_data = [
            {
                "order_id": order_id,
                "product_id": item.get("product_id"),
                "quantity": item.get("quantity"),
                "price": item.get("price")
            }
            for item in products
        ]

        saved = self.orders_products_repository.save_products_in_order({
            "order_id": order_id,
            "products": products_data
        })
        if not saved:
            return False
        return True

    @database_connection
    def get_products_in_order(self, order_id: str):
        all_products = self.orders_products_repository.get_products_in_order(order_id)
        return [product.serialize for product in all_products]

    @database_connection
    def get_order_by_id(self, order_id: str):
        order = self.orders_repository.get(order_id=order_id)
        return order.serialize

    @database_connection
    def get_sales_per_week(self, menu_id: str):
        """
        Retorna a quantidade TOTAL de pedidos por dia da semana (Seg–Dom),
        filtrando somente a semana atual.
        """

        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday())  ## segunda-feira
        end_of_week = start_of_week + timedelta(days=6)  ## domingo

        orders = self.orders_repository.get_orders_between_dates_any_status(
            menu_id=menu_id,
            start_date=start_of_week,
            end_date=end_of_week
        )

        if not orders:
            return [0, 0, 0, 0, 0, 0, 0]

        week_map = {d: 0 for d in range(7)}

        for order in orders:
            weekday = order.created_at.weekday()
            week_map[weekday] += 1

        return [week_map[d] for d in range(7)]