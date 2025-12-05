from flask import Blueprint

api = Blueprint("api", __name__, url_prefix="/api")
vws = Blueprint("vws", __name__)

from source.app.blueprints.api.cart import *
from source.app.blueprints.api.customers import *
from source.app.blueprints.api.customers import  *
from source.app.blueprints.api.analysis import *
from source.app.blueprints.api.tokens import *
from source.app.blueprints.api.stores import *
from source.app.blueprints.api.menus import *
from source.app.blueprints.api.products import *
from source.app.blueprints.api.categories import *
from source.app.blueprints.api.orders import *
from source.app.blueprints.api.authorizations import *

from source.app.blueprints.frontend.dashboard import *
from source.app.blueprints.frontend.integrations import *
from source.app.blueprints.frontend.statistics import *
from source.app.blueprints.frontend.client import *
from source.app.blueprints.frontend.home import *