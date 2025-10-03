from source.app.repository.stores_repository import StoresRepository
from source.app.utils.jwt import *
from source.app.exceptions.stores_exceptions import *
from source.app.exceptions.authorizations_exceptions import *
from source.app.settings.logging_settings import get_logger
from source.app.utils.passwords import *
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import time

logger = get_logger(__name__)


class AuthorizationsServices:
    def __init__(self):
        self.stores_repository = StoresRepository()


    def verify_store_credentials(self, email: str, password: str):
        logger.info(f"Checking if email '{email}' exists in the database.")
        store = self.stores_repository.find_by_email(email)

        if not store:
            logger.warning(f"No email '{email}' found.")
            raise StoresNotFoundException("Comércio não encontrado.")

        if not verify_password(password=password, hashed_password=store.password):
            logger.warning(f"Password for '{email}' does not match.")
            raise InvalidPasswordException("Senhas não são iguais.")

        expiration_time = datetime.now(ZoneInfo("America/Sao_Paulo")) + timedelta(minutes=60)
        exp_timestamp = int(expiration_time.timestamp())
        token_issuer = "Orkestro"

        claims = {
            "iss": token_issuer,
            "sub": store.serialize["id"],
            "role": "COMMON",
            "exp": exp_timestamp
        }

        access_token = generate_token(claims)
        logger.info(f"Access token created successfully: {access_token}")

        return access_token

