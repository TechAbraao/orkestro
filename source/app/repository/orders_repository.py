from source.app.settings.definitions_settings import db as database
from source.app.utils.decorators.database import transactional
from sqlalchemy.exc import SQLAlchemyError
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