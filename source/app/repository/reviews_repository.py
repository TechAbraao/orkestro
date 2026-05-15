from source.app.entities.reviews_entity import ReviewsEntity
from source.app.settings.definitions_settings import db as database
from source.app.utils.decorators.database import transactional

class ReviewsRepository():

    def __init__(self):
        self.session = database.session
        self.dir_name = "reviews_repository.py"

    @transactional
    def add(self, entity):
        self.session.add(entity)
        return True