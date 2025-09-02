from source.app.repository.menus_repository import MenusRepository
from source.app.entities.menus_entity import MenusEntity
from source.app.decorators.database import database_connection
from uuid import uuid4
from source.app.exceptions.menu_exceptions import *
from datetime import datetime
from zoneinfo import ZoneInfo
from source.app.settings.logging_settings import get_logger
from source.app.repository.categories_repository import CategoriesRepository

logger = get_logger(__name__)

class MenuServices:
    def __init__(self):
        self.menu_repository = MenusRepository()
        self.category_repository = CategoriesRepository()
        self.menu_entity = MenusEntity()
    
    @database_connection
    def create_menu(self, data) -> bool:
        """ Create a new Menu """

        entity = MenusEntity(
            id=uuid4(),
            name=data.get("name"),
            description=data.get("description"),
            created_at=datetime.now(ZoneInfo("America/Sao_Paulo"))
        )
        
        self.menu_repository.save(entity)
        return True

    @database_connection
    def get_all_menus(self, include=None):
        menus = self.menu_repository.all()
        result = []

        for menu in menus:
            menu_data = menu.serialize
            if include == "categories":
                categories = self.category_repository.find_by_menu_id(menu.id)
                menu_data["categories"] = [c.serialize for c in categories]
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
        updated = self.menu_repository.update(menu_id, data)

        if not updated:
            raise MenuNotFoundException("Menu not found.")
