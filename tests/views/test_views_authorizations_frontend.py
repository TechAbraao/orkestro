import pytest
from tests.conftest import client
from source.app.utils.jwt import *

@pytest.mark.views
@pytest.mark.auth
def test_view_authorizations_not_logged_dashboard(client):
    """
    Cenário: Usuário não logado tenta acessar a rota /dashboard.

    Comportamento esperado:
    - A rota deve redirecionar para a página de login (/signin)
    - O status code do redirect deve ser 302
    """
    response = client.get("/dashboard")
    redirect_url = response.headers.get("Location")

    assert response.status_code == 302
    assert redirect_url == '/signin'

@pytest.mark.views
@pytest.mark.auth
def test_view_authorizations_not_logged_profile(client):
    """
    Cenário: Usuário não logado tenta acessar a rota /profile.

    Comportamento esperado:
    - A rota deve redirecionar para a página de login (/signin)
    - O status code do redirect deve ser 302
    """

    response = client.get("/profile")
    redirect_url = response.headers.get("Location")

    assert response.status_code == 302
    assert redirect_url == '/signin'

@pytest.mark.views
@pytest.mark.auth
def test_view_authorizations_not_logged_orders(client):
    """
    Cenário: Usuário não logado tenta acessar a rota /orders.

    Comportamento esperado:
    - A rota deve redirecionar para a página de login (/signin)
    - O status code do redirect deve ser 302
    """

    response = client.get("/orders")
    redirect_url = response.headers.get("Location")

    assert response.status_code == 302
    assert redirect_url == '/signin'

@pytest.mark.views
@pytest.mark.auth
def test_view_authorizations_not_logged_menus(client):
    """
    Cenário: Usuário não logado tenta acessar a rota /menus.

    Comportamento esperado:
    - A rota deve redirecionar para a página de login (/signin)
    - O status code do redirect deve ser 302
    """

    response = client.get("/menus")
    redirect_url = response.headers.get("Location")

    assert response.status_code == 302
    assert redirect_url == '/signin'

