from source.app.settings.definitions_settings import db as database
from source.app.utils.decorators.database import transactional
from source.app.entities.stores_entity import StoresEntity

class StoresRepository:
    def __init__(self):
        self.session = database.session

    @transactional
    def save(self, store: StoresEntity) -> StoresEntity:
        self.session.add(store)
        return store

    def find_by_id(self, store_id: int) -> StoresEntity | None:
        return self.session.get(StoresEntity, store_id)

    def find_by_unique_fields(self, email: str, name: str, telephone: str):
        return (
            self.session
            .query(StoresEntity)
            .filter(
                (StoresEntity.email == email) |
                (StoresEntity.name == name) |
                (StoresEntity.telephone == telephone)
            )
            .first()
        )

    def find_all(self) -> list[StoresEntity]:
        return self.session.query(StoresEntity).all()

    @transactional
    def update(self, store: StoresEntity, **kwargs) -> StoresEntity:
        for key, value in kwargs.items():
            if hasattr(store, key):
                setattr(store, key, value)
        self.session.add(store)
        return store

    @transactional
    def delete(self, store: StoresEntity) -> None:
        self.session.delete(store)
