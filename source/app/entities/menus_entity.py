
from source.app.settings.definitions_settings import db as database
from datetime import datetime
from zoneinfo import ZoneInfo

class MenusEntity(database.Model):
    """ Entity Model for Menus """
    __tablename__ = "menus"

    id = database.Column(database.UUID(as_uuid=True), primary_key=True)
    name = database.Column(database.String(100), nullable=False)
    description = database.Column(database.String(255), nullable=True)
    created_at = database.Column(
        database.DateTime,
        nullable=False,
        default=lambda: datetime.now(ZoneInfo("America/Sao_Paulo"))
    )

    """ Relationships 1:N with CategoriesEntity """
    categories = database.relationship(
        "CategoriesEntity", 
        back_populates="menu", 
        cascade="all, delete-orphan",  
        lazy="select" 
    )

    @property
    def serialize(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            # "categories": [c.serialize for c in self.categories]
        }