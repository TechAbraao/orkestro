from flask import Blueprint

### Implementação no futuro do projeto.
api = Blueprint("api", __name__)
vws = Blueprint("vws", __name__)

### Importações necessárias para os endpoints.
from source.app.blueprints.frontend import *