from source.app import create_app
import pytest

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({"TESTING": True})
    yield app


@pytest.fixture()
def client(app):
    with app.app_context():
        with app.test_client() as client:
            yield client