from source.app.repository.stores_repository import StoresRepository
from source.app.entities.stores_entity import StoresEntity
from source.app.settings.logging_settings import get_logger
from source.app.exceptions.stores_exceptions import *
from source.app.utils.passwords import *
import uuid

logger = get_logger(__name__)

class StoresServices:
    def __init__(self):
        self.stores_repository = StoresRepository()

    def create_new_account(self, account_data) -> bool:
        email = account_data.get("email")
        if not email or not account_data.get("password") or not account_data.get("telephone"):
            raise ValueError("Email, password and telephone are required")

        existing_store = self.stores_repository.find_by_unique_fields(
            email, account_data.get("name"), account_data.get("telephone")
        )

        logger.info("Hashing the password")
        hashed_password = hash_password(account_data["password"])


        logger.info("Checking for conflicts with store name, phone number and email")
        if existing_store:
            conflict_fields = []
            if existing_store.email == email:
                conflict_fields.append("email")
            if existing_store.name == account_data.get("name"):
                conflict_fields.append("name")
            if existing_store.telephone == account_data.get("telephone"):
                conflict_fields.append("telephone")
            raise StoresDuplicateException(f"Conflict with fields: {', '.join(conflict_fields)}")

        account = StoresEntity(
            id=uuid.uuid4(),
            name=account_data.get("name", "Undefined"),
            email=email,
            password=hashed_password,
            telephone=account_data.get("telephone", "Undefined")
        )

        logger.info(f"Saving new store with email {email}")
        self.stores_repository.save(account)
        return True
