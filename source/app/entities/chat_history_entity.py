from source.app.settings.definitions_settings import db as database


class ChatHistory(database.Model):
    __tablename__ = "chat_histories"

    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    session_id = database.Column(database.String, nullable=False)
    message = database.Column(database.JSON, nullable=False)