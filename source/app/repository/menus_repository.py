from source.app.settings.definitions_settings import db as database
from source.app.utils.decorators.database import transactional
from source.app.entities.menus_entity import MenusEntity
from source.app.entities.stores_entity import StoresEntity
from sqlalchemy.orm import raiseload

class MenusRepository:
    def __init__(self):
        self.session = database.session
    
    def all(self):
        return self.session.query(MenusEntity).all()

    def get_by_slug(self, slug: str):
        menu = (
            self.session
            .query(MenusEntity)
            # I was supposed to ignore the products!
            .options(raiseload(MenusEntity.products))
            .filter(MenusEntity.slug == slug)
            .first()
        )

        if not menu:
            return False

        return menu

    @transactional
    def save(self, menu: MenusEntity) -> None:
        self.session.add(menu)
        
    @transactional
    def delete(self, id: str) -> bool:
        menu = self.session.query(MenusEntity).filter_by(id=id).first()
        if menu:
            self.session.delete(menu)
            return True
        return False
    
    @transactional
    def exists(self, id: str) -> bool:
        return self.session.query(MenusEntity).filter(
        MenusEntity.id == id
        ).first() is not None

    def get_by_store_id(self, store_id):
        return (self.session.query(MenusEntity)
                .filter(MenusEntity.store_id == store_id)
                .all())

    def get_specific_menu_by_store_id(self, store_id):
        return (self.session.query(MenusEntity)
                .filter(MenusEntity.store_id == store_id)
                .first())

    @transactional
    def exists_by_store_and_id(self, store_id: str, menu_id: str) -> bool:
        return (
            self.session.query(MenusEntity)
            .filter(
                MenusEntity.id == menu_id,
                MenusEntity.store_id == store_id
            )
            .first()
            is not None
        )

    @transactional
    def exists_menu_by_store_id(self, store_id: str) -> bool:
        return self.session.query(MenusEntity).filter(
            MenusEntity.store_id == store_id
        ).first() is not None

    @transactional
    def update(self, menu_id: str, data) -> bool:
        menu = (
            self.session
            .query(MenusEntity)
            .filter_by(id=menu_id)
            .first()
        )

        if not menu:
            return False  

        allowed_fields = {"name", "description", "slug"}
        for key, value in data.items():
            if key in allowed_fields:
                setattr(menu, key, value)
                
        return True

    def get(self, menu_id: str):
        return (
            self
            .session
            .query(MenusEntity)
            .filter(
                MenusEntity.id == menu_id
            ).first()
        )

    @transactional
    def update_status(self, menu_id: str, activated: bool) -> bool:
        menu = self.session.query(MenusEntity).filter_by(id=menu_id).first()
        if not menu:
            return False

        menu.activated = activated
        return True
