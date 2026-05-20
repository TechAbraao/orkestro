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

    def all(self):
        return self.session.query(ReviewsEntity).all()
    
    def get_reviews_by_to(self, to: str):
        return self.session.query(ReviewsEntity).filter_by(
            to=to
        ).all()