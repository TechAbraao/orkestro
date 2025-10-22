from source.app.settings.definitions_settings import db as database
from source.app.utils.decorators.database import transactional
from source.app.entities.opening_hours_entity import OpeningHoursEntity
from sqlalchemy.orm import Session
from sqlalchemy import delete

class OpeningHoursRepository:
    def __init__(self):
        self.session = database.session

    @transactional
    def save_many(self, data):
        self.session.add_all(data)

    def get_hours_in_menu(self, menu_id):
        return self.session.query(OpeningHoursEntity).filter(OpeningHoursEntity.menu_id == menu_id).all()

    def exists_hours_in_menu(self, menu_id):
        exists = (
            self.session.query(OpeningHoursEntity)
            .filter(OpeningHoursEntity.menu_id == menu_id)
            .first()
        )
        return exists is not None

    """ Estudar a fundo esse 'synchronize_session=False'. """
    """ Aparentemente ele é mais otimizado pra acessar o banco de dados. """
    @transactional
    def delete_all_hours(self, menu_id: int) -> int:
        deleted_count = self.session.query(OpeningHoursEntity).filter(
            OpeningHoursEntity.menu_id == menu_id
        ).delete(synchronize_session=False)
        return deleted_count

    @transactional
    def update(self, id, data):
        pass
