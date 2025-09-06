from functools import wraps
from source.app.settings.definitions_settings import db
from sqlalchemy.exc import OperationalError
from source.app.exceptions.database_exceptions import DatabaseUnavailableException

def transactional(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            db.session.commit()
            return result
        except Exception as e:
            db.session.rollback()
            raise e
    return wrapper

def database_connection(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except OperationalError as err:
            raise DatabaseUnavailableException(details=err)
    return wrapper
