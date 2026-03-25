from flask import request, abort, jsonify
from source.app.blueprints.routes import api
from source.app.settings.logging_settings import get_logger
from source.app.services import stores_services
from source.app.utils.responses import Response
from source.app.schemas import stores_schemas
from werkzeug.exceptions import UnprocessableEntity

logger = get_logger(__name__)
dir_name = 'stores.py'

@api.route("/stores", methods=["POST"])
def api_post_stores():
    body = request.get_json()
    body_validated = stores_schemas.load(body)

    roles = body.get("roles", None)
    allowed_roles = {"COMMON", "PRIVILEGED"}
    if not roles or not set(roles).issubset(allowed_roles):
        abort(UnprocessableEntity.code, "Insira uma role válida, são elas: ['COMMON', 'PRIVILEGED']")

    store = stores_services.create_store(body)

    return jsonify({"message": "Loja criada com sucesso.", "status_code": 201})

""" EM CONSTRUÇÃO """
@api.route("/stores", methods=["GET"])
def api_get_store():
    slug = request.args.get("slug", "N/A")
    if slug and slug != "N/A":
        logger.info(f"[{dir_name}] Request Params (slug): '{slug}'")
        store = stores_services.get_store_by_slug(slug)
        if store:
            logger.info(f"[{dir_name}] Loja encontrado para o slug '{slug}'")
            return jsonify({
                "message": f"Loja encontrada através do '{slug}'.",
                "data": store,
                "status_code": 200
            })
        else:
            return jsonify({
                "message": f"Nenhum cardápio encontrado para o slug '{slug}'.",
                "status_code" : 404
            })

    all_stores = stores_services.all_stores()
    return Response.success(
        message="Lista de todos os comércios.",
        data=stores_schemas.dump(all_stores, many=True),
        status_code=200
    )

@api.route("/stores/<string:store_id>", methods=["PUT"])
def api_put_stores():
    # TODO: Implementar a modificação de LOJAS

    return jsonify({
        "message": "",
        "status_code": 200
    })

@api.route("/stores/<string:store_id>", methods=["DELETE"])
def api_delete_stores():
    # TODO: Implementar deletar LOJAS

    return jsonify({
        "message": "",
        "status_code": 200
    })