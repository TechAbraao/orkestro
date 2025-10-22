from source.app.settings.definitions_settings import db as database
from datetime import time
import uuid

class OpeningHoursEntity(database.Model):
    __tablename__ = "opening_hours"

    id = database.Column(database.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    day = database.Column(database.String(20), nullable=False)
    open = database.Column(database.Time, nullable=True)
    close = database.Column(database.Time, nullable=True)

    menu_id = database.Column(
        database.UUID(as_uuid=True),
        database.ForeignKey("menus.id", ondelete="CASCADE"),
        nullable=False
    )

    menu = database.relationship("MenusEntity", back_populates="opening_hours")

    @property
    def serialize(self):
        return {
            "id": str(self.id),
            "day": self.day,
            "open": self.open.strftime("%H:%M") if self.open else None,
            "close": self.close.strftime("%H:%M") if self.close else None,
            "menu_id": self.menu_id
        }
