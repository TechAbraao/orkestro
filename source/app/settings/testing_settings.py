import os
from dotenv import load_dotenv
from source.app.settings.database_settings import postgres_settings

load_dotenv()

class Config(object):
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True

class DevelopmentConfig(Config):
    FLASK_DEBUG = True
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = postgres_settings.get_uri()

class TestingConfig(Config):
    TESTING = True
    DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False

def get_flask_config(env):
    if env == "development":
        return DevelopmentConfig()
    elif env == "testing":
        return TestingConfig()