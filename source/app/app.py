from source.app import create_app
from source.app.settings.application_settings import application_settings as settings
from source.app.extesions.socket_io import socketio

app = create_app()

if __name__ == "__main__":
    socketio.run(
        app,
        host=settings.FLASK_HOST,
        port=settings.FLASK_PORT,
        debug=settings.FLASK_DEBUG,
        use_reloader=False,
        allow_unsafe_werkzeug=True
    )
