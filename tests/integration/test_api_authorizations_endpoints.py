import logging

class TestApiAuthorizationsEndpoints:
    @classmethod
    def setup_class(cls):
        logging.disable(logging.CRITICAL)

    # Verificando se o 'signup' está funcionando.
    def test_api_signup(self, client):
        pass
