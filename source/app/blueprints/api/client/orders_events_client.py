from source.app.extesions.socket_io import socketio
from flask_socketio import emit

@socketio.on('connect')
def handle_welcome_message():
    emit("welcome", {"msg": "Welcome to Orkestro."})

