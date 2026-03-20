from source.app.settings.logging_settings import get_logger
from source.app.utils.decorators.database import database_connection
from source.app.entities.products_entity import ProductsEntity
from source.app.repository.products_repository import ProductsRepository
from source.app.repository.categories_repository import CategoriesRepository
from source.app.exceptions.products_exceptions import *
from flask import url_for, current_app
from source.app.exceptions.category_exceptions import *
import uuid

logger = get_logger()
dir_name = 'products_services.py'

class ProductsServices:
    def __init__(self):
        self.products_repository = ProductsRepository()
        self.category_repository = CategoriesRepository()

    @database_connection
    def create(self, product_body, category_id):
        exists = self.products_repository.exists(
            name=product_body["name"],
            category_id=category_id
        )
        if exists:
            logger.warning(f"Product with name '{product_body['name']}' exists in this category with id '{category_id}'.")
            raise ProductDuplicateNameException("Duplicate product name in the same category.")

        image_url = product_body.get("url_image", None)
        if image_url is None:
            logger.warning(f"Nenhuma imagem disponibilizada, usando a URL padrão.")
            with current_app.app_context():
                image_url = url_for('static', filename='images/default-product.png', _external=True)

        product = ProductsEntity(
            id = uuid.uuid4(),
            name=product_body.get("name"),
            description=product_body.get("description"),
            price=product_body.get("price"),
            category_id=category_id,
            image_url=image_url,
            activated=True
        )

        saved_product = self.products_repository.create(
            category_id=category_id,
            product_data=product
        )

        if not saved_product:
            logger.warning(
                f"Failed to create product with name '{product_body.get('name')}' "
                f"in category '{category_id}'."
            )
            raise ProductCreationException("Error creating product.")

        logger.info(f"Product '{product_body.get('name')}' created successfully in category '{category_id}'.")
        return True

    @database_connection
    def update(self, product_body, product_id):
        update = self.products_repository.update(
            data=product_body,
            entity_id=product_id
        )
        if not update:
            raise ProductNotFoundException("Product not found.")

        return True

    @database_connection
    def find_all_by_category_id(self, category_id):
        products = self.products_repository.find_by_category_id(category_id)

        if not products:
            logger.warning(f"Category with id '{category_id}' not found or has no products.")
            raise CategoryNotFoundException("Category not found or empty.")

        products_serialized = [product.serialize for product in products]

        logger.info(f"All products returned in category id '{category_id}'.")
        return products_serialized

    @database_connection
    def get_by_id(self, product_id: str):
        product = (
            self
            .products_repository
            .get(
                product_id=product_id
            )
        )
        if not product:
            logger.warning(f"Product with id '{product_id}' not found.")
            raise ProductNotFoundException("Product not found.")

        return product.serialize

    @database_connection
    def update_by_id(self, product_id: str, activated: bool) -> bool:
        return self.products_repository.update_status_by_id(product_id, activated)

    @database_connection
    def delete(self, product_id: str):
        deleted = (
            self
            .products_repository
            .delete(
            product_id=product_id
        ))
        logger.info(f"[{dir_name}] Verificando se o produto foi deletado: {deleted}")
        if not deleted:
            logger.warning(f"[{dir_name}] Produto com UUI = '{product_id}' não encontrado.")
            raise ProductNotFoundException("Produto não encontrado.")
        return True