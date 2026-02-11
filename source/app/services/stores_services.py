from source.app.repository.stores_repository import StoresRepository
from source.app.repository.menus_repository import MenusRepository
from source.app.entities.stores_entity import StoresEntity
from source.app.settings.logging_settings import get_logger
from source.app.utils.decorators.database import database_connection
from source.app.exceptions.stores_exceptions import *
from source.app.utils.passwords import *
from flask import url_for, current_app
import uuid

logger = get_logger(__name__)

class StoresServices:
    def __init__(self):
        self.stores_repository = StoresRepository()
        self.menus_services = MenusRepository()

    @database_connection
    def create_new_account(self, account_data) -> bool:
        email = account_data.get("email")
        if not email or not account_data.get("password") or not account_data.get("telephone"):
            raise ValueError("E-mail, telefone e senha são campos obrigatórios.")

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

        logger.warning("No logoo image URL provided, using default image URL.")
        with current_app.app_context():
            logo_url = url_for('static', filename='images/default-store-logo.png', _external=False)

        account = StoresEntity(
            id=uuid.uuid4(),
            name=account_data.get("name", "Undefined"),
            email=email,
            password=hashed_password,
            telephone=account_data.get("telephone", "Undefined"),
            logo_url=f"{logo_url}"
        )

        logger.info(f"Saving new store with email {email}")
        self.stores_repository.save(account)
        return True

    @database_connection
    def about_me_store_account(self, store_id: str):
        store = self.stores_repository.find_by_id(store_id)
        return store.serialize_frontend

    @database_connection
    def get_store_by_slug(self, slug: str):
        store_by_slug = self.stores_repository.find_store_by_menu_slug(slug)
        if store_by_slug:
            return store_by_slug.serialize
        return None

    @database_connection
    def get_menu_by_store_id(self, store_id):
        menu_by_store_id = self.menus_services.get_specific_menu_by_store_id(store_id)
        if not menu_by_store_id:
            return {"id": ""}
        return menu_by_store_id.serialize