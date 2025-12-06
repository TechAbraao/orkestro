from source.app.entities.stores_entity import StoresEntity
from source.app.entities.menus_entity import MenusEntity
from source.app.utils.passwords import *
from pytest import mark
import logging
from faker import Faker
import uuid
fake = Faker()

@mark.api
class TestApiAuthorizationsEndpoints:
    @classmethod
    def setup_class(cls):
        logging.disable(logging.CRITICAL)

    @mark.auth
    def test_api_signup(self, client, db):
        """
        Testa o endpoint '/api/signup' para criação de uma nova loja.

        Cenário:
            - Uma loja com nome, e-mail, telefone e senha é enviada via POST.

        Verifica:
            - O status code retornado é 200 (OK).
            - A mensagem de retorno é 'Loja criada com sucesso.'
        """
        data = {
            "name": fake.company(),
            "email": fake.unique.email(),
            "telephone": str(fake.numerify(text="#########")),
            "password": fake.password(length=10)
        }

        res = client.post("/api/signup", json=data)
        res_json = res.get_json()

        assert res.status_code == 200, f"Erro ao receber status code: {res.status_code}"
        assert res_json["message"] == "Loja criada com sucesso."

    @mark.auth
    def test_signup_and_login(self, client, db):
        """
        Testa a criação de uma loja e o login do usuário em sequência.

        Cenário:
            1. Cria uma loja diretamente no banco de dados com senha hashed.
            2. Cria um menu associado a essa loja.
            3. Realiza login via endpoint '/api/signin' usando e-mail e senha.

        Verifica:
            - O status code do login é 200 (OK).
            - A mensagem de retorno é 'User authenticated successfully'.
            - O header 'Set-Cookie' está presente na resposta.
            - O cookie 'access_token' é definido corretamente nos headers.
        """
        password_plain = fake.password(length=10)
        store_id = uuid.uuid4()
        store = StoresEntity(
            id=store_id,
            name=fake.company(),
            email=fake.unique.email(),
            password=hash_password(password_plain),
            telephone=str(fake.numerify(text="#########")),
        )
        db.session.add(store)
        db.session.commit()

        menu = MenusEntity(
            name="Menu Teste",
            store_id=store_id
        )
        db.session.add(menu)
        db.session.commit()

        login_data = {
            "email": store.email,
            "password": password_plain
        }

        res_signin = client.post("/api/signin", json=login_data)
        res_signin_json = res_signin.get_json()
        cookie_header = res_signin.headers["Set-Cookie"]

        assert res_signin.status_code == 200, f"Erro: {res_signin.status_code}"
        assert res_signin_json["message"] == "User authenticated successfully"
        assert "Set-Cookie" in res_signin.headers
        assert cookie_header.startswith("access_token=")

