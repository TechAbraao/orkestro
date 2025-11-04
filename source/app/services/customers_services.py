from source.app.repository.customers_repository import CustomersRepository
from source.app.utils.decorators.database import database_connection
from source.app.entities.users_entity import UsersEntity
from source.app.settings.logging_settings import get_logger
import uuid

logger = get_logger(__name__)

class CustomersServices:
    def __init__(self):
        self.customers_repository = CustomersRepository()

    @database_connection
    def add_customer(self, body) -> bool:
        user = UsersEntity(
            id=str(uuid.uuid4()),
            name=body.get("name", "N/A"),
            telephone=body.get("telephone", "N/A"),
            address=body.get("address", "N/A"),
            house_number=body.get("number", 0)
        )

        created_user = self.customers_repository.save(user)
        if not created_user:
            return False
        if not created_user:
            return False
        return True

    @database_connection
    def find_by_id(self, customer_id):
        user = self.customers_repository.find(customer_id=customer_id)
        if not user:
            raise ValueError("Nenhum cliente encontrado.")
        return user.serialize