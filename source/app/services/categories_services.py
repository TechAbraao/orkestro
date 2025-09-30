from source.app.repository.categories_repository import CategoriesRepository
from source.app.repository.menus_repository import MenusRepository
from source.app.repository.redis_repository import RedisRepository
from source.app.settings.logging_settings import get_logger
from source.app.entities.categories_entity import CategoriesEntity
from source.app.utils.decorators.database import database_connection
from source.app.exceptions.category_exceptions import *
from source.app.utils.cache_keys import *
from source.app.exceptions.menu_exceptions import *
from flask import url_for, current_app
import uuid


logger = get_logger(__name__)

class CategoriesServices:
    def __init__(self):
        self.categories_repository = CategoriesRepository()
        self.menus_repository = MenusRepository()
        self.redis_repository = RedisRepository()

    @database_connection
    def create_category(self, menu_id: str, category_data: dict) -> bool:
        exists_category_name = self.categories_repository.exists_category_name_in_menu(menu_id, category_data.get("name"))
        if exists_category_name:
            logger.error(f"Category '{category_data.get('name')}' already exists in this menu.")
            raise CategoryDuplicateNameException("Category name already exists in this menu.")
        
        image_url = category_data.get("url_image", None)
        if image_url is None:
            logger.warning(f"Nenhuma imagem disponibilizada, usando a URL padrão.")
            with current_app.app_context():
                image_url = url_for('static', filename='images/default-category.png', _external=True)
        
        logger.info("Criando uma nova Categoria no Repository.")
        category_entity = CategoriesEntity(
            id=str(uuid.uuid4()),
            name=category_data.get("name", None),
            description=category_data.get("description", None),
            menu_id=menu_id,
            url_image=image_url
        )
        saved_category = self.categories_repository.create_category(category_entity)


        logger.info(f"Estratégia de atualizar o cacheamento no Cardápio '{menu_id}'.")
        searching_menu = self.menus_repository.get(menu_id)
        menu_slug = searching_menu.slug
        logger.info(f"Você encontrou o Slug '{menu_slug}' no Cardápio '{menu_id}'.")
        cache_key_del = get_cache_key_by_slug(slug=menu_slug, include_products=False, include_categories=True)
        delete_cache = self.redis_repository.delete(cache_key_del)
        if delete_cache:
            logger.info(f"Cache do Slug '{menu_slug}' deletado com sucesso. A chave do cache é '{cache_key_del}'.")


        logger.info(f"Category created successfully.")
        return saved_category

    @database_connection
    def get_all_categories_by_menu(self, menu_id: str):

        exists_menu = self.menus_repository.exists(menu_id)
        if not exists_menu:
            logger.warning(f"No menu found whose id is '{menu_id}'")
            raise MenuNotFoundException(f"Menu with id '{menu_id}' not found.")

        categories_by_menu = self.categories_repository.get_categories_by_menu_id(menu_id)
        if not categories_by_menu:
            logger.warning(f"No category found in menu whose id is '{menu_id}'")
            raise CategoryNotFoundException(f"No categories registered in menu with id '{menu_id}'")

        return categories_by_menu

    @database_connection
    def get_category_by_id(self, category_id: str):
        logger.info(f"Accessing category service layer to fetch category with ID '{category_id}'")

        category = self.categories_repository.get_category_by_id(category_id)

        if not category:
            logger.warning(f"Category whose id is '{category_id}' not found.")
            raise CategoryNotFoundException("Category not found.")

        return category.serialize

    @database_connection
    def delete_category_by_id(self, category_id: str):
        logger.info(f"Acessando a camada de serviços das Categorias cujo 'category_id' é: '{category_id}'.")

        logger.info(f"Obtendo informações do Cardápio através do 'category_id' igual '{category_id}'.")
        menu_info = self.categories_repository.get_menu_by_category_id(category_id)
        if not menu_info:
            raise MenuNotFoundException("Menu not found for this category.")

        menu_id = menu_info["menu_id"]
        menu_name = menu_info["menu_name"]

        logger.info(f"Estratégia de atualizar o cacheamento no Cardápio '{menu_id}'.")
        searching_menu = self.menus_repository.get(menu_id)
        menu_slug = searching_menu.slug
        logger.info(f"Você encontrou o Slug '{menu_slug}' no Cardápio '{menu_id}'.")
        cache_key_del = get_cache_key_by_slug(slug=menu_slug, include_products=False, include_categories=True)
        delete_cache = self.redis_repository.delete(cache_key_del)
        if delete_cache:
            logger.info(f"Cache do Slug '{menu_slug}' deletado com sucesso. A chave do cache é '{cache_key_del}'.")

        deleted = self.categories_repository.delete_category(category_id)
        if not deleted:
            logger.warning(f"Category whose id is '{category_id}' not found.")
            raise CategoryNotFoundException("Category not found.")

        return True

    @database_connection
    def change_category_by_id(self, category_data, category_id: str):
        logger.info(f"Accessing category service layer to change category with ID '{category_id}'.")

        category = (
            self
            .categories_repository
            .get_category_by_id(category_id)
        )

        if not category:
            logger.warning(f"Category whose id is '{category_id}' not found.")
            raise CategoryNotFoundException("Category not found.")


        changed_category = (
            self
            .categories_repository
            .update(
                category_data=category_data,
                category_id=category_id
            )
        )

        return True

    @database_connection
    def get_category_by_id_and_slug(self, slug: str, category_id: str):
        category = self.categories_repository.get_category_by_slug_and_id(slug, category_id)
        if not category:
            raise CategoryNotFoundException(f"Category '{category_id}' not found for menu '{slug}'")
        return category.serialize
