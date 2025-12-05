# tests/conftest.py
import pytest
from source.app import create_app
from source.app.settings.definitions_settings import db as _db
from pathlib import Path

""" App de Testes. """
@pytest.fixture(scope="session")
def app():
    app = create_app("testing")
    return app

""" Client pos Teste. """
@pytest.fixture(scope="function")
def client(app):
    return app.test_client()

""" Schema para cada teste de derruba depois, garantindo o isolamento. """
@pytest.fixture(scope="function")
def db(app):
    with app.app_context():
        _db.create_all()
        try:
            yield _db
        finally:
            _db.session.remove()
            _db.drop_all()
