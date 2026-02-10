from flask_socketio import SocketIO

socketio = SocketIO(
    async_mode="eventlet",
    cors_allowed_origins=[
        "http://localhost:3000",
        "http://localhost:5173"
    ]
)

def init_socketio(app):
    """Inicijalizuj SocketIO sa Flask aplikacijom"""
    socketio.init_app(app)
    print("✅ WebSocket inicijalizovan")
    return socketio