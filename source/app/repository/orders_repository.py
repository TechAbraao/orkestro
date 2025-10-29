from source.app.settings.definitions_settings import db as database
from source.app.utils.decorators.database import transactional

class OrdersRepository:
    def __init__(self):
        self.session = database.session

    @transactional
    def create_order(self, data: dict):
        pass