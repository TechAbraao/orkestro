from source.app.settings.definitions_settings import db as database
from source.app.utils.decorators.database import transactional
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from source.app.entities.orders_entity import OrderEntity
from source.app.entities.menus_entity import MenusEntity

class OrdersRepository:
    def __init__(self):
        self.session = database.session

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