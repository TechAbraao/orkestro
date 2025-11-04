from source.app.settings.definitions_settings import db as database
from source.app.utils.decorators.database import transactional
from source.app.entities.users_entity import UsersEntity

class CustomersRepository:
    def __init__(self):
        self.session = database.session

    @transactional
    def save(self, customer: UsersEntity):
        self.session.add(customer)
        return True

    def find(self, customer_id):
        return (
            self.session
            .query(UsersEntity)
            .filter(UsersEntity.id == customer_id)
        ).first()