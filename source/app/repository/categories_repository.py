from source.app.entities.categories_entity import CategoriesEntity
from source.app.settings.definitions_settings import db as database
from source.app.decorators.database import transactional    
from source.app.settings.logging_settings import get_logger
from sqlalchemy import func


logger = get_logger(__name__)

class CategoriesRepository:
    def __init__(self):
        self.session = database.session

    def get_category_by_id(self, category_id):
        logger.info(f"Fetching category with ID '{category_id}' from the database")
        category =  (
            self.session
            .query(CategoriesEntity)
            .filter(CategoriesEntity.id == category_id)
            .first()
        )
        return category

    def exists_category_name_in_menu(self, menu_id, category_name):
        return (
            self.session
            .query(CategoriesEntity)
            .filter(
                CategoriesEntity.menu_id == menu_id,
                func.lower(CategoriesEntity.name) == category_name.lower()
            )
            .first()
            is not None
        )
    
    @transactional
    def create_category(self, category_entity: CategoriesEntity):
        logger.info("Adding new category to the database.")
        self.session.add(category_entity)
        return category_entity

    def find_by_menu_id(self, menu_id):
        return (
            self.session.query(CategoriesEntity)
            .filter(CategoriesEntity.menu_id == menu_id)
            .all()
        )
    
    @transactional
    def update_category(self, category_id, name=None, description=None):
        pass
    
    @transactional
    def delete_category(self, category_id) -> bool:
        category = (
            self.session.query(CategoriesEntity)
            .filter(CategoriesEntity.id == category_id)
            .first()
        )
        if not category:
            return False

        self.session.delete(category)
        return True

    def get_categories_by_menu_id(self, menu_id: str):
        categories = (
            self.session
            .query(CategoriesEntity)
            .filter(CategoriesEntity.menu_id == menu_id)
            .all()
        )
        logger.info("Query performed on the categories table.")
        return [category.serialize for category in categories]

    @transactional
    def update(self, category_id, category_data) -> bool:

        logger.info(f"Fetching category with ID '{category_id}' from the database")
        category = (
            self.session
            .query(CategoriesEntity)
            .filter_by(id=category_id)
            .first()
        )

        if not category:
            logger.warning(f"Category whose id is '{category_id}' not found.")
            return False

        allowed_fields = {"name", "description", "url_image"}
        for key, value in category_data.items():
            if key in allowed_fields:
                setattr(category, key, value)

        return True