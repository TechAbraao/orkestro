from source.app.repository.orders_repository import OrdersRepository
from source.app.repository.orders_products_repository import OrdersProductsRepository
from source.app.services import orders_services
from source.app.utils.decorators.database import database_connection
from source.app.entities.orders_entity import OrderEntity
from datetime import datetime, timedelta, timezone
from source.app.settings.logging_settings import get_logger
from uuid import uuid4

logger = get_logger(__name__)

class OrdersServices:
    def __init__(self):
        self.orders_repository = OrdersRepository()
        self.orders_products_repository = OrdersProductsRepository()
        self.dir_name = 'orders_services.py'

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
            [*] Início: segunda-feira, 00:00:00+00
            [*] Fim: domingo, 23:59:59.99999+00
            [*] Exemplo:
                [*] segunda-feira: 2025-11-17 00:00:00+00
                [*] domingo: 2025-11-23 23:59:59.999999+00
        """

        today = datetime.now(timezone.utc).date()
        logger.info(f"[{self.dir_name}] Data de hoje: {today}")

        start_of_week = datetime.combine(
            today - timedelta(days=today.weekday()),
            datetime.min.time(),
            tzinfo=timezone.utc
        )

        logger.info(f"[{self.dir_name}] Início da semana (segunda-feira): {start_of_week}")

        end_of_week = datetime.combine(
            start_of_week.date() + timedelta(days=6),
            datetime.max.time(),
            tzinfo=timezone.utc
        )
        logger.info(f"[{self.dir_name}] Último dia da semana (domingo): {end_of_week}")

        orders = self.orders_repository.get_orders_between_dates_any_status(
            menu_id=menu_id,
            start_date=start_of_week,
            end_date=end_of_week
        )

        logger.info(f"[{self.dir_name}] Pedidos no período (segunda-feira até domingo): {orders}")

        week_map_count = {d: 0 for d in range(7)}
        week_map_total_values = {d: 0 for d in range(7)}

        if not orders:
            return [0] * 7, [0] * 7

        logger.info(f"[{self.dir_name}] Pedidos organizados pela semana: {week_map_count}")
        logger.info(f"[{self.dir_name}] Valores totais organizados pela semana: {week_map_count}")

        for order in orders:
            weekday = order.created_at.weekday()
            week_map_count[weekday] += 1
            week_map_total_values[weekday] += order.total_value

        return [week_map_count[d] for d in range(7)], [week_map_total_values[d] for d in range(7)]
