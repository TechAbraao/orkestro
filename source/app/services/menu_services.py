from source.app.repository.products_repository import ProductsRepository
from source.app.repository.menus_repository import MenusRepository
from source.app.entities.menus_entity import MenusEntity
from source.app.utils.decorators.database import database_connection
from uuid import uuid4
from source.app.exceptions.menu_exceptions import *
from datetime import datetime
from zoneinfo import ZoneInfo
from source.app.settings.logging_settings import get_logger
from source.app.repository.categories_repository import CategoriesRepository
from source.app.utils.slugs import slug_generator

logger = get_logger(__name__)

class MenuServices:
    def __init__(self):
        self.menu_repository = MenusRepository()
        self.category_repository = CategoriesRepository()
        self.products_repository = ProductsRepository()
        self.menu_entity = MenusEntity()


    @database_connection
    def create_menu(self, data) -> bool:

        slug = slug_generator(data.get("name"))
        entity = MenusEntity(
            id=uuid4(),
            name=data.get("name"),
            description=data.get("description"),
            created_at=datetime.now(ZoneInfo("America/Sao_Paulo")),
            slug=slug
        )
        
        self.menu_repository.save(entity)
        return True

    @database_connection
    def get_all_menus(self, include=None):
        menus = self.menu_repository.all()
        result = []

        for menu in menus:
            menu_data = menu.serialize

            if include and "categories" in include:
                categories = self.category_repository.find_by_menu_id(menu.id)
                menu_data["categories"] = [c.serialize for c in categories]

            if include and "products" in include:
                products = self.products_repository.find_by_menu_id(menu.id)
                menu_data["products"] = [p.serialize for p in products]

            result.append(menu_data)

        return result

    @database_connection
    def delete_menu(self, menu_id: str) -> None:
        exists = self.menu_repository.exists(menu_id)
        if not exists:
            raise MenuNotFoundException("Menu not found.")
        self.menu_repository.delete(menu_id)    
        
    @database_connection
    def update_menu(self, menu_id: str, data) -> None:
        data["slug"] = slug_generator(data.get("name"))

        updated = self.menu_repository.update(menu_id, data)

        if not updated:
            raise MenuNotFoundException("Menu not found.")

    @database_connection
    def get_menu_by_slug(self, slug: str):
        menu = self.menu_repository.get_by_slug(slug)
        if not menu:
            logger.warning(f"Menu with slug {slug} not found.")
            raise MenuNotFoundException("Menu not found.")

        logger.info(f"Menu with slogan '{slug}' found")
        return menu.serialize_client