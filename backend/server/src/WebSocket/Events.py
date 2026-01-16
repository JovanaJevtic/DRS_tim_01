from flask_socketio import emit, join_room, leave_room
from WebSocket.SocketConfig import socketio

@socketio.on('connect')
def handle_connect():
    """Kada se klijent konektuje"""
    print(f"🟢 Klijent se konektovao")
    emit('connection_response', {'message': 'Uspešno konektovan na WebSocket server'})

@socketio.on('disconnect')
def handle_disconnect():
    """Kada se klijent diskonektuje"""
    print(f"🔴 Klijent se diskonektovao")

@socketio.on('join_user_room')
def handle_join_user_room(data):
    """Korisnik se pridružuje svojoj privatnoj sobi za notifikacije"""
    user_id = data.get('user_id')
    if user_id:
        room = f"user_{user_id}"
        join_room(room)
        print(f"👤 Korisnik {user_id} se pridružio sobi: {room}")
        emit('room_joined', {'room': room, 'message': f'Pridružili ste se sobi {room}'})

@socketio.on('leave_user_room')
def handle_leave_user_room(data):
    """Korisnik napušta svoju privatnu sobu"""
    user_id = data.get('user_id')
    if user_id:
        room = f"user_{user_id}"
        leave_room(room)
        print(f"👤 Korisnik {user_id} napustio sobu: {room}")

def emit_role_changed(user_id, new_role):
    """Emituj event kada admin promeni ulogu korisnika"""
    room = f"user_{user_id}"
    socketio.emit('role_changed', {
        'user_id': user_id,
        'new_role': new_role,
        'message': f'Vaša uloga je promenjena u {new_role}'
    }, room=room)
    print(f"📢 Emitovan event: role_changed za korisnika {user_id}")
