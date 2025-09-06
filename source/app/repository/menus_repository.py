from source.app.settings.definitions_settings import db as database
from source.app.utils.decorators.database import transactional
from source.app.entities.menus_entity import MenusEntity

class MenusRepository:
    def __init__(self):
        self.session = database.session
    
    def all(self):
        """ Retrieve all menu records from the database """
        return self.session.query(MenusEntity).all()

    def get_by_slug(self, slug: str):
        menu = (
            self.session
            .query(MenusEntity)
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
