from source.app import create_app
from source.app.settings.application_settings import application_settings as settings

app = create_app()

if __name__ == "__main__":
    app.run(
        host=settings.FLASK_HOST,
        port=settings.FLASK_PORT,
        debug=settings.FLASK_DEBUG
    )
