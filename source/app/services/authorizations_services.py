from source.app.repository.stores_repository import StoresRepository
from source.app.utils.jwt import *
from source.app.exceptions.stores_exceptions import *
from source.app.exceptions.authorizations_exceptions import *
from source.app.settings.logging_settings import get_logger
from source.app.services.menu_services import MenuServices
from source.app.utils.passwords import *
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import time

logger = get_logger(__name__)

class AuthorizationsServices:
    def __init__(self):
        self.stores_repository = StoresRepository()
        self.menu_services = MenuServices()
        self.dir_name = 'authorizations_services.py'

    def verify_store_credentials(self, email: str, password: str):
        logger.info(f"[{self.dir_name}] Verificando e-mail já está cadastrado: '{email}'.")
        store = self.stores_repository.find_by_email(email)

        if not store:
            logger.warning(f"[{self.dir_name}] Nenhum e-mail: '{email}' encontrado.")
            raise StoresNotFoundException("Comércio não encontrado.")

        if not verify_password(password=password, hashed_password=store.password):
            logger.warning(f"[{self.dir_name}] As senhas do '{email}' não correspondem.")
            raise InvalidPasswordException("Erro ao autenticar comércio.")

        expiration_time = datetime.now(ZoneInfo("America/Sao_Paulo")) + timedelta(minutes=60)
        exp_timestamp = int(expiration_time.timestamp())
        token_issuer = "Orkestro"

        logger.info(f"[{self.dir_name}] O comércio têm 'store_id' = '{store.serialize["id"]}'.")
        menu_id = self.menu_services.get_menu_id_by_store_id(store.serialize["id"])
        logger.info(f"[{self.dir_name}] Através do 'store_id', encontrou o 'menu_id' = '{menu_id}'.")

        claims = {
            "iss": token_issuer,
            "sub": str(store.serialize["id"]),
            "menu_id": menu_id if menu_id is not None else "",
            "role": "COMMON",
            "exp": exp_timestamp
        }

        access_token = generate_token(claims)
        logger.info(f"[{self.dir_name}] Token de acesso criado com sucesso: {access_token}")

        return access_token
