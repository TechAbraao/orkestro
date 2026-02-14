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
    ## Parâmetros: store (a loja), roles do token, tempo de expiração, quem assinou o token)
    def _generate_access_token(self, store, role: str, exp_timestamp: int, token_issuer: str):
        store_id = store.serialize["id"]
        logger.info(f"[{self.dir_name}] O comércio tem 'store_id' = '{store_id}'.")

        menu_id = self.menu_services.get_menu_id_by_store_id(store_id)
        logger.info(f"[{self.dir_name}] Através do 'store_id', encontrou o 'menu_id' = '{menu_id}'.")



        claims = {
            "iss": token_issuer,
            "sub": str(store_id),
            "menu_id": menu_id if menu_id is not None else "",
            "roles": role,
            "exp": exp_timestamp
        }

        access_token = generate_token(claims)
        logger.info(f"[{self.dir_name}] Token de acesso criado com sucesso.")

        return access_token

    def verify_store_credentials(self, email: str, password: str, hasAdmin: bool = False):
        EXPIRATION_TIME = datetime.now(ZoneInfo("America/Sao_Paulo")) + timedelta(minutes=60)
        TIMESTAMP = int(EXPIRATION_TIME.timestamp())
        ISSUER = "Orkestro"

        ## Cenário: Se o 'hasAdmin' = True, o login é realizado pelo administrador. ##
        if hasAdmin:
            logger.info(f"[{self.dir_name}] | Credencial de administrador: email={email} e password={password}")

            ## Cenário: Verificando se o administrador está persistido no banco de dados. ##
            store_admin = self.stores_repository.find_by_email(email)
            logger.info(f"[{self.dir_name}] | Encontrou credencial de administrador: {store_admin}")

            ## Cenário: Caso o 'store_admin' retorne None, implica que o administrador não está persistido no banco de dados. ##
            if store_admin is None:
                logger.info(f"[{self.dir_name}] | Nenhuma credencial do adm encontrada, ou seja, salvando credencial do administrador")

                ## Cenário: Informações que serão persistida no banco de dados sobre o administrador. ##
                roles_required = ["ADMIN"]
                data = {
                    "name": "administrator",
                    "email": email,
                    "password": password,
                    "telephone": "000000000",
                    "roles": roles_required
                }

                saved_admin = self.stores_services.create_store(account=data)
                logger.info(f"[{self.dir_name}] | Usuário administrado criado com sucesso.")

                ## Cenário: Caso, por alguma razão, o usuário administrador não seja persistido no banco de dados. ##
                if not saved_admin:
                    abort(500, "Erro ao criar usuario administrador")

                ## Cenário: Atualizando as informações do 'store_admin'. ##
                store_admin = saved_admin

            if not verify_password(password=password, hashed_password=store_admin.password):
                logger.warning(f"[{self.dir_name}] As senhas do '{email}' não correspondem.")
                raise InvalidPasswordException("Erro ao autenticar comércio.")

            logger.info(f"[{self.dir_name}] O comércio têm 'store_id' = '{store_admin.serialize['id']}'.")

            # Criando o Token de Acesso com Role ADMIN
            access_token = self._generate_access_token(
                store=store_admin, role=store_admin.roles, exp_timestamp=TIMESTAMP, token_issuer=ISSUER
            )
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

        access_token = self._generate_access_token(
            store=store, role=store.roles, exp_timestamp=TIMESTAMP, token_issuer=ISSUER
        )

        return access_token

