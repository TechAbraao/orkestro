from source.app.blueprints.routes import api

common = "/api/stores/<string:store_id>/employees"

@api.route(common, methods=["GET"])
def get_employees():
    pass

@api.route(common, methods=["POST"])
def post_employees():
    pass

@api.route(f"{common}/<string:employee_id>", methods=["DELETE"])
def delete_employees(store_id, employee_id):
    pass

@api.route(f"{common}/<string:employee_id>", methods=["PUT"])
def put_employees(store_id, employee_id):
    pass
