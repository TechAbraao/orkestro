from source.app.settings.database_settings import postgres_settings
from source.app.settings.definitions_settings import db, ma
from source.app.handlers.handlers_exceptions import register_error_handlers
from source.app.blueprints import menus_bp, categories_bp, products_bp, menus_client, orders_client
from flask import Flask
from flask_migrate import Migrate
from flasgger import Swagger
import yaml
from pathlib import Path


def create_app() -> Flask:
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = postgres_settings.get_uri()

    BASE_DIR = Path(__file__).resolve().parent
    SWAGGER_PATH = BASE_DIR / "swagger.yml"

    db.init_app(app)
    ma.init_app(app)
    Migrate(app, db)

    swagger = Swagger(app, template_file=str(SWAGGER_PATH))

    def load_template():
        with open(SWAGGER_PATH, "r") as f:
            return yaml.safe_load(f)

    @app.before_request
    def reload_swagger():
        app.config['SWAGGER'] = load_template()
        swagger.template = app.config['SWAGGER']

    from source.app.entities.associations_tables_entity import menu_product

    from source.app.entities.users_entity import UsersEntity
    from source.app.entities.menus_entity import MenusEntity
    from source.app.entities.products_entity import ProductsEntity
    from source.app.entities.categories_entity import CategoriesEntity
    from source.app.entities.orders_entity import OrderEntity
    from source.app.entities.orders_products_entity import OrderProductsEntity
    from source.app.entities.chat_history_entity import ChatHistory

    app.register_blueprint(menus_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(menus_client)
    app.register_blueprint(orders_client)

    register_error_handlers(app)

    return app
