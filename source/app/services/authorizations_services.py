from alembic.util import status
from source.app.repository.stores_repository import StoresRepository
from flask import abort
from source.app.utils.jwt import *
from source.app.exceptions.stores_exceptions import *
from source.app.exceptions.authorizations_exceptions import *
from source.app.settings.logging_settings import get_logger
from source.app.services.menu_services import MenuServices
from source.app.services.stores_services import StoresServices
from source.app.utils.passwords import *
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


logger = get_logger(__name__)

class AuthorizationsServices:
    def __init__(self):
        self.stores_repository = StoresRepository()
        self.stores_services = StoresServices()
        self.menu_services = MenuServices()
        self.dir_name = 'authorizations_services.py'

    """ Método privado para criar tokens de acesso """
    # TODO: implementar futuramente para melhorar o fluxo do método verify_store_credentials
    def _generate_access_token(self, store, role: str, exp_timestamp: int, token_issuer: str):
        store_id = store.serialize["id"]
        logger.info(f"[{self.dir_name}] O comércio tem 'store_id' = '{store_id}'.")

        menu_id = self.menu_services.get_menu_id_by_store_id(store_id)
        logger.info(f"[{self.dir_name}] Através do 'store_id', encontrou o 'menu_id' = '{menu_id}'.")

        claims = {
            "iss": token_issuer,
            "sub": str(store_id),
            "menu_id": menu_id if menu_id is not None else "",
            "roles": [role],
            "exp": exp_timestamp
        }

        access_token = generate_token(claims)
        logger.info(f"[{self.dir_name}] Token de acesso criado com sucesso.")

        return access_token

    def verify_store_credentials(self, email: str, password: str, role: str, hasAdmin: bool = False):
        expiration_time = datetime.now(ZoneInfo("America/Sao_Paulo")) + timedelta(minutes=60)
        exp_timestamp = int(expiration_time.timestamp())
        token_issuer = "Orkestro"

        # Aqui vai verificar se é administrador ou não
        if hasAdmin:
            logger.info(f"[{self.dir_name}] | Credencial de administrador: email={email} e password={password}")

            store_admin = self.stores_repository.find_by_email(email)
            logger.info(f"[{self.dir_name}] | Encontrou credencial de administrador: {store_admin}")

            if store_admin is None:
                logger.info(f"[{self.dir_name}] | Nenhuma credencial do adm encontrada, ou seja, salvando credencial do administrador")

                data = {
                    "name": "administrator",
                    "email": email,
                    "password": password,
                    "telephone": "000000000",
                }

                saved_admin = self.stores_services.create_new_account(account_data=data)
                logger.info(f"[{self.dir_name}] | Usuário administrado criado com sucesso.")
                if not saved_admin:
                    abort(500, "Erro ao criar usuario administrador")

            if not verify_password(password=password, hashed_password=store_admin.password):
                logger.warning(f"[{self.dir_name}] As senhas do '{email}' não correspondem.")
                raise InvalidPasswordException("Erro ao autenticar comércio.")

            logger.info(f"[{self.dir_name}] O comércio têm 'store_id' = '{store_admin.serialize["id"]}'.")
            menu_id = self.menu_services.get_menu_id_by_store_id(store_admin.serialize["id"])
            logger.info(f"[{self.dir_name}] Através do 'store_id', encontrou o 'menu_id' = '{menu_id}'.")

            roles_credential = []
            roles_credential.append(role)
            claims = {
                "iss": token_issuer,
                "sub": str(store_admin.serialize["id"]),
                "menu_id": menu_id if menu_id is not None else "",
                "roles": roles_credential,
                "exp": exp_timestamp
            }

            access_token = generate_token(claims)
            logger.info(f"[{self.dir_name}] Token de acesso criado com sucesso: {access_token}")

            return access_token

        # Ai agora verifica outras coisas
        logger.info(f"[{self.dir_name}] Verificando e-mail já está cadastrado: '{email}'.")
        store = self.stores_repository.find_by_email(email)

        if not store:
            logger.warning(f"[{self.dir_name}] Nenhum e-mail: '{email}' encontrado.")
            raise StoresNotFoundException("Comércio não encontrado.")

        if not verify_password(password=password, hashed_password=store.password):
            logger.warning(f"[{self.dir_name}] As senhas do '{email}' não correspondem.")
            raise InvalidPasswordException("Erro ao autenticar comércio.")

        logger.info(f"[{self.dir_name}] O comércio têm 'store_id' = '{store.serialize["id"]}'.")
        menu_id = self.menu_services.get_menu_id_by_store_id(store.serialize["id"])
        logger.info(f"[{self.dir_name}] Através do 'store_id', encontrou o 'menu_id' = '{menu_id}'.")

        roles_credential = []
        roles_credential.append(role)
        claims = {
            "iss": token_issuer,
            "sub": str(store.serialize["id"]),
            "menu_id": menu_id if menu_id is not None else "",
            "roles": roles_credential,
            "exp": exp_timestamp
        }

        access_token = generate_token(claims)
        logger.info(f"[{self.dir_name}] Token de acesso criado com sucesso: {access_token}")

        return access_token

