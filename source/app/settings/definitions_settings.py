from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

"""
Database Definition (Flask-SQLAlchemy Lib) 
"""
db = SQLAlchemy()
""" 
Schemas Definition (Flask-Marshmallow Lib)
"""
ma = Marshmallow()