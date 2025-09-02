from source.app.settings.definitions_settings import db as database
from datetime import datetime
from zoneinfo import ZoneInfo

class CategoriesEntity(database.Model):
    """ Entity Model for Categories """
    __tablename__ = "categories"
    __table_args__ = (
        database.UniqueConstraint('menu_id', 'name', name='uix_menu_category'),
    )
    
    
    id = database.Column(database.UUID(as_uuid=True), primary_key=True)
    name = database.Column(database.String, nullable=False)
    description = database.Column(database.String, nullable=True)
    url_image = database.Column(database.String(255), nullable=True)
    created_at = database.Column(
        database.DateTime,
        nullable=False,
        default=lambda: datetime.now(ZoneInfo("America/Sao_Paulo"))
    )
    menu_id = database.Column(
        database.UUID(as_uuid=True),
        database.ForeignKey("menus.id", ondelete="CASCADE"),
        nullable=False
    )
    """ Relationship N:1 with MenusEntity """
    
    menu = database.relationship(
        "MenusEntity",
        back_populates="categories"
    )

    @property
    def serialize(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "menu_id": str(self.menu_id),
            "url_image": self.url_image
        }
