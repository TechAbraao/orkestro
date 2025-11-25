from flask import request
from source.app.blueprints.routes import api
from source.app.settings.logging_settings import get_logger
from source.app.services import stores_services
from source.app.utils.responses import Response

logger = get_logger(__name__)
dir_name = 'stores.py'

@api.route("/stores", methods=["GET"])
def api_get_store():
    slug = request.args.get("slug", "N/A")
    if slug and slug != "N/A":
        logger.info(f"[{dir_name}] Request Params (slug): '{slug}'")
        store = stores_services.get_store_by_slug(slug)
        if store:
            logger.info(f"[{dir_name}] Loja encontrado para o slug '{slug}'")
            return Response.success(
                message=f"Loja encontrada através do '{slug}'.",
                data=store,
                status_code=200
            )
        else:
            return Response.error(
                message=f"Nenhum cardápio encontrado para o slug '{slug}'.",
                status_code=404
            )

    all_stores = "TODO (futura implementação)"
    return Response.success(
        message="Lista de todos os comércios.",
        data=all_stores,
        status_code=200
    )