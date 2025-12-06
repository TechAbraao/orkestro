import logging
from pytest import mark

@mark.vws
class TestVwsPublicEndpoints:
    @classmethod
    def setup_class(cls):
        logging.disable(logging.CRITICAL)

    # Verificando se as principais rotas públicas renderizam corretamente.
    def test_vws_public_endpoints_are_available(self, client):
        endpoints = ["/home", "/signin", "/signup"]
        for endpoint in endpoints:
            res = client.get(endpoint)
            assert res.status_code == 200, f"Falha ao acessar '{endpoint}'."

    # Verificando se a rota '/' redireciona para '/home'.
    def test_vws_endpoint_root_resolves_to_home(self, client):
        res = client.get("/")

        assert res.status_code == 302
        assert "Location" in res.headers
        assert res.headers["Location"].endswith("/home")