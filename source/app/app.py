import os
from source.app import create_app
from source.app.settings.application_settings import application_settings as settings
from source.app.extesions.socket_io import socketio

app = create_app()

debug_mode = settings.FLASK_DEBUG or os.environ.get("PYCHARM_HOSTED") == "1"

if __name__ == "__main__":
    async_mode = "threading" if debug_mode else "eventlet"
    socketio.init_app(app, async_mode=async_mode)
    socketio.run(
        app,
        host=settings.FLASK_HOST,
        port=settings.FLASK_PORT,
        debug=settings.FLASK_DEBUG,
        use_reloader=False,
        allow_unsafe_werkzeug=True
    )
