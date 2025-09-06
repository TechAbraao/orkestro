from typing import Any, List, Optional
from source.app.settings.definitions_settings import db as database
from source.app.entities.products_entity import ProductsEntity
from source.app.entities.categories_entity import CategoriesEntity
from source.app.utils.decorators.database import transactional
from source.app.settings.logging_settings import get_logger
from source.app.utils.contracts.crud_interface import CRUDInterface
from source.app.entities.associations_tables_entity import menu_product

logger = get_logger()

class ProductsRepository(CRUDInterface):
    def __init__(self):
        self.session = database.session

    def get(self, product_id: str) -> Optional[ProductsEntity]:
        return (self.session
                .query(ProductsEntity)
                .filter(ProductsEntity.id == product_id)
                .first())

    def all(self) -> List[ProductsEntity]:
        return (
            self.session
            .query(ProductsEntity)
            .all()
        )

    def find_by_category_id(self, category_id: str) -> List[ProductsEntity]:
        """
        Returns all products that belong to a specific category.
        """
        return (
            self.session.query(ProductsEntity)
            .filter(ProductsEntity.category_id == category_id)
            .all()
        )

    def exists(self, name: str, category_id: str) -> bool:
        """
        Checks if a product with the same name already exists in the same category.
        Returns true if it exists, false otherwise.
        """
        return (
                self.session.query(ProductsEntity)
                .join(CategoriesEntity)
                .filter(
                    ProductsEntity.name == name,
                    ProductsEntity.category_id == category_id
                )
                .first()
                is not None
        )

    @transactional
    def create(self, product_data: dict, category_id: str) -> Any:
        logger.info(f"Fetching category with ID '{category_id}' from the database")
        category = (self.session.query(CategoriesEntity).filter(CategoriesEntity.id == category_id).first())

        if not category:
            logger.warning(f"Category whose id is '{category_id}' not found.")
            return False

        category.products.append(product_data)

        return True


    @transactional
    def update(self, entity_id: str, data: dict) -> bool:
        """
        Updates a product in the database by its ID.
        """
        logger.info(f"Attempting to update product with ID '{entity_id}'")

        product = (
            self.session.query(ProductsEntity)
            .filter(ProductsEntity.id == entity_id)
            .first()
        )

        if not product:
            logger.warning(f"Product with ID '{entity_id}' not found.")
            return False

        for key, value in data.items():
            if hasattr(product, key):
                setattr(product, key, value)

        logger.info(f"Product with ID '{entity_id}' updated successfully.")
        return True


    @transactional
    def delete(self, product_id: str) -> bool:
        """
        Deletes a product from the database by its ID.
        """

        logger.info(f"Attempting to delete product with ID '{product_id}'")

        product = (
            self.session.query(ProductsEntity)
            .filter(ProductsEntity.id == product_id)
            .first()
        )

        if not product:
            logger.warning(f"Product with ID '{product_id}' not found.")
            return False

        self.session.delete(product)

        logger.info(f"Product with ID '{product_id}' deleted successfully.")
        return True
    def find_by_menu_id(self, menu_id: str) -> List[ProductsEntity]:
        return (
            self.session.query(ProductsEntity)
            .join(menu_product, ProductsEntity.id == menu_product.c.product_id)
            .filter(menu_product.c.menu_id == menu_id)
            .all()
        )
