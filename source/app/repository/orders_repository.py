from source.app.settings.definitions_settings import db as database
from source.app.utils.decorators.database import transactional
from source.app.settings.logging_settings import get_logger
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from datetime import datetime, timedelta
from source.app.entities.orders_entity import OrderEntity
from source.app.entities.menus_entity import MenusEntity

logger = get_logger(__name__)

class OrdersRepository:
    def __init__(self):
        self.session = database.session
        self.dir_name = 'orders_repository.py'

    @transactional
    def create_order(self, data: OrderEntity) -> bool:
        self.session.add(data)
        return True

    def get_order_by_menu_id(self, menu_id):
        orders = self.session.query(OrderEntity).filter_by(menu_id=menu_id).all()
        return orders

    @transactional
    def delete_by_order_id(self, order_id):
        order = self.session.query(OrderEntity).filter_by(id=order_id).first()
        if not order:
            return False
        self.session.delete(order)
        return True

    @transactional
    def update_status_by_order_id(self, status, order_id):
        try:
            order = self.session.query(OrderEntity).filter_by(id=order_id).first()
            if not order:
                return None

            order.status = status
            self.session.add(order)
            return order

        except SQLAlchemyError as e:
            print(f"Erro ao atualizar status: {str(e)}")
            return None

    def count_orders_by_status(self, menu_id, status):
        return self.session.query(OrderEntity).filter_by(menu_id=menu_id, status=status).count()

    @transactional
    def next_order_number(self, menu_id):
        """
        Essa função filtra os pedidos de terminado 'menu_id' e, a partir disso, pega o
        valor (não objeto) do maior número, com o '.scalar()' é incrementa.
        """
        last_number = (
            self.session.query(func.max(OrderEntity.order_number))
            .filter(OrderEntity.menu_id == menu_id)
            .scalar()
        )
        """ Aqui ocorre o incremento. """
        return (last_number or 0) + 1

    def get(self, order_id):
        return self.session.query(OrderEntity).filter_by(id=order_id).first()

    def get_orders_between_dates_any_status(self, menu_id, start_date, end_date):
        orders = (
            self.session.query(OrderEntity)
            .filter(
                OrderEntity.menu_id == menu_id,
                OrderEntity.created_at >= start_date,
                OrderEntity.created_at <= end_date
            )
            .all()
        )
        logger.info(f"[{self.dir_name}] Através do banco de dados, obtém-se: {orders}")
        return orders

    def number_of_orders_placed(self, menu_id):
        """Retorna o maior número de pedidos (order_number) de um cardápio."""
        max_value = (
            self.session.query(func.max(OrderEntity.order_number))
            .filter(OrderEntity.menu_id == menu_id)
            .scalar()
        )
        return max_value

    def get_total_sales_last_24h(self, menu_id):
        now = datetime.utcnow()
        logger.info(f"Horário atual: '{now}'")

        last_24h = now - timedelta(hours=24)
        logger.info(f"Cálculo do período de 24h: '{last_24h}'")

        total = (
            self.session.query(func.sum(OrderEntity.total_value))
            .filter(OrderEntity.created_at >= last_24h)
            .filter(OrderEntity.menu_id == menu_id)
            .scalar()
        )

        return total or 0
