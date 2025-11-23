from flask import Blueprint

### Implementação no futuro do projeto.
api = Blueprint("api", __name__, url_prefix="/api")
vws = Blueprint("vws", __name__)

### Camada da API
from source.app.blueprints.api.cart import *
from source.app.blueprints.api.customers import *
from source.app.blueprints.api.customers import  *
from source.app.blueprints.api.analysis import *

### Camada da UI
from source.app.blueprints.frontend.integrations import *
from source.app.blueprints.frontend.statistics import *
