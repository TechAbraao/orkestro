from source.app.utils.responses import Response
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import *
from source.app.exceptions.database_exceptions import *
from source.app.exceptions.menu_exceptions import *
from source.app.exceptions.category_exceptions import *
from source.app.exceptions.products_exceptions import *
from source.app.settings.logging_settings import get_logger

logger = get_logger(__name__)

def register_error_handlers(app):
    """ All error handlers are registered here """
    @app.errorhandler(ValidationError)
    def handle_validation_error(err):
        logger.warning(f"Validation error: {err.messages}")
        response = Response.error(
            message=None,
            errors=err.messages,
            status_code=BadRequest.code
        )
        return response
    @app.errorhandler(DatabaseUnavailableException)
    def handle_database_unavailable(err):
        logger.error(f"Database unavailable: {str(err.details)}")   
        response = Response.error(
            message="Database is unavailable.",
            errors=str(err.details),
            status_code=503
        )
        return response
    @app.errorhandler(MenuNotFoundException)
    def handle_menu_not_found(err):
        logger.warning(f"Menu not found: {str(err.message)}") 
        response = Response.error(
            errors=str(err.message),
            status_code=NotFound.code
        )
        return response
    @app.errorhandler(Exception)
    def handle_generic_exception(err):
        status_code = getattr(err, "code", 500)
        logger.error(f"An error occurred: {str(err)}")
        return Response.error(
            message=str(err),
            errors=None,
            status_code=status_code
        )
    @app.errorhandler(CategoryDuplicateNameException)
    def handle_category_duplicate_name(err):
        logger.warning(f"Category duplicate name: {str(err.message)}") 
        response = Response.error(
            errors=str(err.message),
            status_code=Conflict.code
        )
        return response
    @app.errorhandler(CategoryCreationException)
    def handle_category_creation_exception(err):
        logger.error(f"Category creation failed: {str(err.message)}") 
        response = Response.error(
            errors=str(err.message),
            status_code=InternalServerError.code
        )
        return response
    @app.errorhandler(CategoryNotFoundException)
    def handle_category_not_found_exception(err):
        logger.warning(f"Category not found: {str(err.message)}")
        response = Response.error(
            errors=str(err.message),
            status_code=InternalServerError.code
        )
        return response

    @app.errorhandler(ProductDuplicateNameException)
    def handle_product_duplicate_name_exception(err):
        logger.warning(f"Product duplicate name: {str(err.message)}")
        response = Response.error(
            errors=str(err.message),
            status_code=Conflict.code
        )
        return response

    @app.errorhandler(ProductNotFoundException)
    def handle_product_not_found_exception(err):
        logger.warning(f"Product not found: {str(err.message)}")
        response = Response.error(
            errors=str(err.message),
            status_code=NotFound.code
        )
        return response

    @app.errorhandler(ProductsNotFoundException)
    def handle_products_not_found_exception(err):
        logger.warning(f"Products not found: {str(err.message)}")
        response = Response.error(
            errors=str(err.message),
            status_code=NotFound.code
        )
        return response