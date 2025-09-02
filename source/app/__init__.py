from source.app.settings.database_settings import postgres_settings
from source.app.settings.definitions_settings import *
from source.app.handlers.handlers_exceptions import *
from source.app.blueprints import *
from flask import Flask
from flask_migrate import Migrate
from flasgger import Swagger
import yaml
from pathlib import Path
import os

def create_app() -> Flask:
    app = Flask(__name__)

    from source.app.entities.menus_entity import MenusEntity
    from source.app.entities.categories_entity import CategoriesEntity
    
    app.config['SQLALCHEMY_DATABASE_URI'] = postgres_settings.get_uri()
    
    BASE_DIR = Path(__file__).resolve().parent
    SWAGGER_PATH = BASE_DIR / "swagger.yml"

    swagger = Swagger(app, template_file=str(SWAGGER_PATH))
    db.init_app(app)
    ma.init_app(app)
    Migrate(app, db)

    def load_template():
        with open(SWAGGER_PATH, "r") as f:
            return yaml.safe_load(f)

    @app.before_request
    def reload_swagger():
        app.config['SWAGGER'] = load_template()
        swagger.template = app.config['SWAGGER']
        
    app.register_blueprint(menus_bp)
    app.register_blueprint(categories_bp)
        
    register_error_handlers(app)
    return app