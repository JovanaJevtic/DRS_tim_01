from flask_socketio import SocketIO

socketio = SocketIO(cors_allowed_origins="http://localhost:5173")

def init_socketio(app):
    """Inicijalizuj SocketIO sa Flask aplikacijom"""
    socketio.init_app(app, cors_allowed_origins="http://localhost:5173")
    print("✅ WebSocket inicijalizovan")
    return socketio