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
from source.app.repository.redis_repository import RedisRepository
from source.app.utils.cache_keys import get_cache_key_by_slug

logger = get_logger(__name__)

class MenuServices:
    def __init__(self):
        self.menu_repository = MenusRepository()
        self.category_repository = CategoriesRepository()
        self.products_repository = ProductsRepository()
        self.menu_entity = MenusEntity()
        self.redis_repository = RedisRepository()

    @database_connection
    def create_menu(self, data) -> bool:
        """
            1. Cada loja pode possuir apenas um único cardápio ativo.
            Ou seja, não é permitido cadastrar mais de um cardápio vinculado à mesma loja.
        """
        logger.info(f"Checking for the existence of a menu in store_id '{data["store_id"]}'")
        exists = self.menu_repository.all()
        if exists:
            logger.warning(f"It is not possible to register more than one menu in store_id '{data["store_id"]}'")
            raise OneMenuPerStoreException("You have already found a registered menu.")

        """
            2. Cada cardápio terá um Slug, que é feito pelo nome.
            Através do Slug, será possível acessar o cardápio.
        """
        slug = slug_generator(data.get("name"))

        entity = MenusEntity(
            id=uuid4(),
            name=data.get("name"),
            description=data.get("description"),
            created_at=datetime.now(ZoneInfo("America/Sao_Paulo")),
            slug=slug,
            store_id=data.get("store_id"),
            activated=False
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
    def exists_menu_by_store_id(self, store_id: str):
        exists = self.menu_repository.exists(store_id)
        if exists:
            return True
        return False

    @database_connection
    def get_menus_by_store_id(self, store_id: str):
        pass

    @database_connection
    def delete_menu(self, menu_id: str) -> None:
        exists = self.menu_repository.exists(menu_id)
        if not exists:
            logger.warning(f"Menu with id '{menu_id}' could not be deleted.")
            raise MenuNotFoundException("Menu not found.")
        menu_object = self.menu_repository.get(menu_id)
        slug = menu_object.slug
        logger.info(f"Getting the slug '{slug}' from the ID current menu '{menu_id}'")

        self.menu_repository.delete(menu_id)
        logger.info(f"Menu with id '{menu_id}' deleted successfully.")

        logger.info(f"Invalidating cache for slug '{slug}'.")
        cache_key = get_cache_key_by_slug(slug=slug, include_products=False, include_categories=True)
        self.redis_repository.delete(cache_key)

    @database_connection
    def update_menu(self, menu_id: str, data) -> None:
        logger.info(f"Looking for old slug for menu id '{menu_id}'.")
        old_menu = self.menu_repository.get(menu_id)

        if not old_menu:
            raise MenuNotFoundException("Menu not found.")

        old_slug = old_menu.slug

        logger.info(f"Generating new slug for menu id '{menu_id}'.")
        data["slug"] = slug_generator(data.get("name"))
        new_slug = data["slug"]

        updated = self.menu_repository.update(menu_id, data)
        if not updated:
            raise MenuNotFoundException("Menu not found during update.")

        if old_slug and old_slug != new_slug:
            old_cache_key = get_cache_key_by_slug(
                slug=old_slug,
                include_products=False,
                include_categories=True,
            )
            self.redis_repository.delete(old_cache_key)
            logger.info(f"Cache invalidated for old slug '{old_cache_key}'.")

        new_cache_key = get_cache_key_by_slug(
            slug=new_slug,
            include_products=False,
            include_categories=True,
        )
        self.redis_repository.delete(new_cache_key)
        logger.info(f"Cache invalidated for new slug '{new_cache_key}'.")

        logger.info(f"Menu id '{menu_id}' updated successfully.")

    @database_connection
    def get_menu_by_slug(self, slug: str):
        EXPIRE: int = (10 * 60)

        cache_key = get_cache_key_by_slug(slug=slug, include_products=False, include_categories=True)
        logger.info(f"Caching key created, it is '{cache_key}'")

        cached_data = self.redis_repository.get(cache_key)
        if cached_data:
            logger.info(f"Cache hit for key {cache_key}.")
            logger.info(f"Cache success in method 'get_menu_by_slug'.")
            return cached_data


        menu = self.menu_repository.get_by_slug(slug)
        if not menu:
            logger.warning(f"Menu with slug {slug} not found.")
            raise MenuNotFoundException("Menu not found.")

        result = menu.serialize_client(include_categories=True, include_products=False)
        self.redis_repository.set(cache_key, result, expire=EXPIRE)
        logger.info(f"Cache set for key {cache_key}.")

        logger.info(f"Menu with slug '{slug}' found.")
        return result