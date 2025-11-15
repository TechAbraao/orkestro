from flask import Blueprint

### Implementação no futuro do projeto.
api = Blueprint("api", __name__, url_prefix="/api")
vws = Blueprint("vws", __name__)

### Api
from source.app.blueprints.api.cart import *

### Front-end
from source.app.blueprints.frontend.integrations import *
from source.app.blueprints.frontend.statistics import *