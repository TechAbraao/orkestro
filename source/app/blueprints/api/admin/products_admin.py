from source.app.settings.logging_settings import get_logger
from source.app.utils.responses import Response
from source.app.schemas import uuid_schema, products_schemas
from source.app.services import products_services
from source.app.utils.decorators.validations import *
from source.app.schemas.products_schemas import ProductUpdateSchema
from flask import Blueprint, request


logger = get_logger()
products_bp = Blueprint("products_bp", __name__, url_prefix="/api")
dir_name = 'products_admin.py'

""" 1. Create Product in a Category. """
@products_bp.route("/categories/<string:category_id>/products", methods=["POST"])
def post_products_in_category(category_id: str):
    logger.info("POST /categories/{categoryId}/products - creating new product in category")

    logger.info("Getting JSON data from request and validating fields")
    body = request.get_json()
    data_validated = products_schemas.load(body)
    uuid_validated = uuid_schema.load({"id": category_id})

    created_product = products_services.create(
        category_id=category_id,
        product_body=body
    )

    logger.info("Product created successfully.")
    return Response.success(
        message="Product created successfully.",
        status_code=200
    )

""" 2. List all Products in a Category. """
@products_bp.route("/categories/<string:category_id>/products", methods=["GET"])
def get_products_in_category(category_id: str):
    logger.info("GET /categories/{categoryId}/products - get all products in category.")

    logger.info("Validating the UUID.")
    uuid_validated = uuid_schema.load({"id": category_id})

    products_in_category = products_services.find_all_by_category_id(
        category_id=category_id
    )

    logger.info(f"Product with id '{category_id}' returned successfully.")
    return Response.success(
        status_code=200,
        message="Product(s) returned successfully.",
        data=products_in_category
    )

""" 3. Get Specific Product """
@products_bp.route("/products/<string:product_id>", methods=["GET"])
def get_product(product_id: str):
    logger.info("GET /products/{productId} - get a specific product.")

    logger.info("Validating the UUID.")
    uuid_validated = uuid_schema.load({"id": product_id})

    product = products_services.get_by_id(product_id=product_id)
    return Response.success(
        message="Product returned successfully.",
        data=product,
        status_code=200
    )

""" 4. Update Specific Product. """
@products_bp.route("/products/<string:product_id>", methods=["PUT"])
# @validate_request(ProductUpdateSchema())
def put_product(product_id: str):
    logger.info("GET /products/{productId} - Changing a specific product.")

    logger.info("Getting JSON data from request and validating fields")
    body = request.get_json()
    data_validated = products_schemas.load(body)
    uuid_validated = uuid_schema.load({"id": product_id})

    changed_product = products_services.update(
        product_id=product_id,
        product_body=body
    )

    return Response.success(
        message="Product changed successfully.",
        status_code=200
    )

""" 5. Deleting Specific Product. """
@products_bp.route("/products/<string:product_id>", methods=["DELETE"])
def delete_product(product_id: str):
    logger.info(f"[{dir_name}] DELETE /products/{product_id} - Deletando um produto específico.")

    logger.info(f"[{dir_name}] Validando o UUID do Produto.")
    uuid_validated = uuid_schema.load({"id": product_id})

    try:
        deleted = products_services.delete(product_id=product_id)
    except ValueError as err:
        logger.error(f"[{dir_name}] Erro ao deletar produto: {err}")
        return Response.error(
            message="Erro ao deletar produto.",
            status_code=400
        )

    return Response.success(
        message="Product deleted successfully.",
        status_code=200
    )

""" 6. List all Products in a Menu (associated categories). """
@products_bp.route("/menus/<string:menu_id>/products", methods=["GET"])
def get_products_in_menu(menu_id: str):
    pass
