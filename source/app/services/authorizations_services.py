from source.app.repository.stores_repository import StoresRepository
from source.app.exceptions.stores_exceptions import *
from source.app.exceptions.authorizations_exceptions import *
from source.app.settings.logging_settings import get_logger
from source.app.utils.passwords import *

logger = get_logger(__name__)

class AuthorizationsServices:
    def __init__(self):
        self.stores_repository = StoresRepository()

    def verify_store_credentials(self, email: str, password: str):
        logger.info(f"Checking if email '{email}' exists in the database.")
        store = self.stores_repository.find_by_email(email)

        if not store:
            logger.warning(f"No email '{email}' found.")
            raise StoresNotFoundException("Store not found.")

        if not verify_password(password=password, hashed_password=store.password):
            logger.warning(f"Password for '{email}' does not match.")
            raise InvalidPasswordException("Passwords are not the same.")

        logger.info(f"Store with id '{store.id}' authenticated successfully.")
        return store
