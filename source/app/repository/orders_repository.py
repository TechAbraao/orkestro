from source.app.settings.definitions_settings import db as database
from source.app.utils.decorators.database import transactional
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