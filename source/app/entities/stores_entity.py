from uuid import uuid4
from source.app.settings.definitions_settings import db as database


class StoresEntity(database.Model):
    __tablename__ = "stores"

    id = database.Column(database.UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = database.Column(database.String(255), nullable=False)
    email = database.Column(database.String(255), unique=True, nullable=False)
    password = database.Column(database.String(255), nullable=False)
    telephone = database.Column(database.String(20), nullable=True)

    menus = database.relationship(
        "MenusEntity",
        back_populates="store",
        cascade="all, delete-orphan"
    )

    @property
    def serialize(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "email": self.email,
            "telephone": self.telephone,
        }