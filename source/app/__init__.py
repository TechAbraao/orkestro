from flask import Flask
from source.app.settings.database_settings import postgres_settings
from source.app.settings.definitions_settings import db, ma
from source.app.handlers.handlers_exceptions import register_error_handlers
from source.app.settings.logging_settings import get_logger
from source.app.blueprints.routes import (vws, api)
from source.app.extesions.socket_io import socketio
from flask_migrate import Migrate
from flasgger import Swagger
import yaml
from pathlib import Path
import os
from flask import request, redirect, url_for, g
from source.app.utils.jwt import decrypt_token

logger = get_logger(__name__)

def create_app(config_name: str = "default"):

    """
        Create and configure the Flask app.
        config_name:
            - "default" (ou "development"/"production") -> usa Postgres definido em postgres_settings
            - "testing" -> testa usando sqlite:///:memory: e configurações de teste
    """
    app = Flask(__name__)

    setup_file = Path(__file__).resolve().parent.parent.parent / "setup.yml"
    with open(setup_file, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    app.config["APPLICATION_VERSION"] = config.get("version")
    logger.info(f"Inicializando o Servidor. Versão: {app.config['APPLICATION_VERSION']}")

    if config_name == "testing":
        # Ambiente de testes: DB em memória, TESTING True e sem CSRF
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        app.config["WTF_CSRF_ENABLED"] = False
        app.config["PROPAGATE_EXCEPTIONS"] = True
    else:
        # Comportamento normal (dev/prod) - usa Postgres configurado
        app.config['SQLALCHEMY_DATABASE_URI'] = postgres_settings.get_uri()

    app.secret_key = os.environ.get("FLASK_SECRET_KEY", "SecretKey")

    BASE_DIR = Path(__file__).resolve().parent
    SWAGGER_PATH = BASE_DIR / "swagger.yml"

    db.init_app(app)
    ma.init_app(app)

    if config_name != "testing":
        Migrate(app, db, directory="source/migrations")
    else:
        logger.debug("Testing mode: skipping Flask-Migrate initialization")

    if config_name != "testing":
        swagger = Swagger(app, template_file=str(SWAGGER_PATH))

        def load_template():
            with open(SWAGGER_PATH, "r") as f:
                return yaml.safe_load(f)
        @app.before_request
        def reload_swagger():
            app.config['SWAGGER'] = load_template()
            swagger.template = app.config['SWAGGER']
    else:
        logger.debug("Testing mode: skipping Swagger initialization")

    from source.app.entities.associations_tables_entity import menu_product

    from source.app.entities.stores_entity import StoresEntity
    from source.app.entities.users_entity import UsersEntity
    from source.app.entities.menus_entity import MenusEntity
    from source.app.entities.products_entity import ProductsEntity
    from source.app.entities.categories_entity import CategoriesEntity
    from source.app.entities.orders_entity import OrderEntity
    from source.app.entities.orders_products_entity import OrderProductsEntity
    from source.app.entities.chat_history_entity import ChatHistory
    from source.app.entities.opening_hours_entity import OpeningHoursEntity

    from source.app.blueprints.api.auth.me_auth import about_auth

    app.register_blueprint(about_auth)

    app.register_blueprint(vws)
    app.register_blueprint(api)

    register_error_handlers(app)

    debug_mode = os.environ.get("FLASK_DEBUG") == "1"
    async_mode = "threading" if debug_mode else "eventlet"
    if config_name != "testing":
        socketio.init_app(app, async_mode=async_mode)
    else:
        logger.debug("Testing mode: skipping socketio initialization")

    try:
        from source.app.blueprints.api import orders_events
    except Exception:
        logger.debug("Could not import orders_events during testing setup (ignoring)")

    @app.before_request
    def apidocs_swagger():
        if request.path.startswith("/apidocs"):

            token = request.cookies.get("access_token")

            if not token:
                auth_header = request.headers.get("Authorization")
                if auth_header and auth_header.startswith("Bearer "):
                    token = auth_header.split(" ")[1]

            if not token:
                return redirect(url_for("vws.views_login"))

            try:
                claims = decrypt_token(token)
            except ValueError:
                return redirect(url_for("vws.views_login"))

            g.jwt_claims = claims

            roles = claims.get("roles", [])
            print("Bora verificar: ", roles)

            if "ADMIN" not in roles:
                return redirect(url_for("vws.views_login"))

    return app
