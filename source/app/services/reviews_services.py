from source.app.repository.reviews_repository import ReviewsRepository
from source.app.repository.stores_repository import StoresRepository
from source.app.utils.decorators.database import database_connection
from source.app.entities.reviews_entity import ReviewsEntity
from flask import url_for, current_app, abort

class ReviewsServices():
    def __init__(self):
        self.reviews_repository = ReviewsRepository()
        self.stores_repository = StoresRepository()

    def add_review(self, body):

        to = body.get("to", "N/A")
        exists_to = self.stores_repository.exists_by_name(to)
        if not exists_to:
            abort(404, description="to não encontrado.")

        # Esse trecho vou comentar, preciso entender um jeito
        # melhor pra fazer essa abordagem.
        """
        by = body.get("by", "N/A")
        exists_bye = self.stores_repository.exists_by_name(by)
        if not exists_bye:
            abort(404, description="by não encontrado.")
        """

        note = body.get("note", "N/A")
        if note < 1 or note > 5:
            abort(400, description="Nota inválida. A nota precisa ser do intervalo: [1, 2, 3, 4, 5]")

        body_to_entity = ReviewsEntity(
            category = body.get("category", "N/A"),
            by = body.get("by", "N/A"),
            description = body.get("description", "N/A"),
            to = body.get("to", "N/A"),
            note = body.get("note", "N/A")
        )
        saved_return = self.reviews_repository.add(body_to_entity)

        if not saved_return:
            abort(
                400,
                description="Erro ao salvar review",
            )

        return True

    @database_connection
    def all_reviews(self):
        all_reviews = self.reviews_repository.all()
        reviews_serialized = [review.serialize for review in all_reviews]
        return reviews_serialized

    @database_connection
    def all_reviews_to(self, name):
        all_reviews_to = self.reviews_repository.get_reviews_by_to(name)
        return all_reviews_to
