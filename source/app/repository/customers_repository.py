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

    def telephone_exists(self, telephone_number):
        return self.session.query(UsersEntity).filter(
            UsersEntity.telephone == telephone_number
        ).first() is not None

    def find_id_by_telephone(self, telephone):
        return (
            self.session
            .query(UsersEntity.id)
            .filter(UsersEntity.telephone == telephone)
            .scalar()
        )
