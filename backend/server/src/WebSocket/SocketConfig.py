from flask_socketio import SocketIO

socketio = SocketIO(
    async_mode="eventlet",
    cors_allowed_origins="*"
)

def init_socketio(app):
    """Inicijalizuj SocketIO sa Flask aplikacijom"""
    socketio.init_app(app)
    print("✅ WebSocket inicijalizovan")
    return socketio