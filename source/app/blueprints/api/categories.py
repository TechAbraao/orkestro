from flask import Blueprint, request
from source.app.settings.logging_settings import get_logger
from source.app.utils.responses import Response
from source.app.schemas import categories_schema, uuid_schema
from source.app.services import categories_services
from werkzeug.exceptions import *
from source.app.blueprints.routes import api

logger = get_logger(__name__)
dir_name = 'categories.py'

""" 01. Create Category in a Menu """
@api.route("/menus/<string:menu_id>/categories", methods=["POST"])
def create_category_in_menu(menu_id: str):
    logger.info("POST /menus/{menu_id}/categories - creating a new category for a menu")

    logger.info("Getting JSON data from request and validating fields")
    body = request.get_json()

    validation_query_params = uuid_schema.load({"id": menu_id})
    validation_body = categories_schema.load(body)

    adding_category = categories_services.create_category(
        menu_id=validation_query_params["id"],
        category_data=body
    )

    if not adding_category:
        logger.error("Failed to create category.")
        return Response.error(
            message="Failed to create category",
            status_code=500
        )

    logger.info("Category created successfully. ID = {adding_category.id}")
    return Response.success(
        message="Category created successfully",
        status_code=201
    ), 201

""" 02. Get Categories from a Menu """
@api.route("/menus/<string:menu_id>/categories", methods=["GET"])
def categories_by_menu(menu_id: str):
    logger.info("GET /menus/{menu_id}/categories - retrieving categories for a menu.")

    validation_query_params = uuid_schema.load({"id": menu_id})
    categories_by_id = categories_services.get_all_categories_by_menu(
        menu_id=menu_id
    )

    logger.info(f"All categories returned by id = {menu_id}")
    return Response.success(
        message="Categories returned successfully.",
        status_code=200,
        data=categories_by_id
    )

""" 03. Get Specific Category """
@api.route("/categories/<string:category_id>", methods=["GET"])
def get_category_by_id(category_id: str):
    logger.info("GET /categories/{category_id} - fetch category by ID.")

    validation_query_params = uuid_schema.load({"id": category_id})
    category = categories_services.get_category_by_id(category_id=category_id)

    return Response.success(
        message="Category returned successfully.",
        status_code=200,
        data=category
    )

""" 04. Delete specific Category """
@api.route("/categories/<string:category_id>", methods=["DELETE"])
def delete_category_by_id(category_id: str):
    logger.info("DELETE /categories/{category_id} - delete category by ID.")

    validation_query_params = uuid_schema.load({"id": category_id})
    deleted = categories_services.delete_category_by_id(
        category_id=validation_query_params["id"]
    )
    if not deleted:
        return Response.error(
            message="Failed to delete category",
            status_code=BadRequest.code
        )

    return Response.success(
        message="Category delete successfully.",
        status_code=200
    )

""" 05. Update Specific Category """
@api.route("/categories/<string:category_id>", methods=["PUT"])
def put_category_by_id(category_id: str):
    logger.info("PUT /categories/{category_id} - change category by ID.")

    logger.info("Getting JSON data from request and validating fields")
    body = request.get_json()
    validation_query_params = uuid_schema.load({"id": category_id})
    validation_body = categories_schema.load(body)

    changed = categories_services.change_category_by_id(
        category_id=validation_query_params["id"],
        category_data=validation_body
    )

    logger.info(f"Category whose ID is '{category_id}' changed successfully.")
    return Response.success(
        message="Category changed successfully.",
        status_code=200
    )
