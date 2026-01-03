import { io, Socket } from 'socket.io-client';

class WebSocketService {
  private socket: Socket | null = null;
  private userId: number | null = null;

  connect(userId: number) {
    if (this.socket?.connected) {
      console.log('⚠️ WebSocket već konektovan');
      return;
    }

    this.userId = userId;
    const SOCKET_URL = import.meta.env.VITE_API_URL.split('/api/v1')[0];

    console.log('🔌 Konektujem se na WebSocket:', SOCKET_URL);

    this.socket = io(SOCKET_URL, {
      transports: ['websocket', 'polling'],
      reconnection: true,
      reconnectionAttempts: 5,
      reconnectionDelay: 1000,
    });

    this.socket.on('connect', () => {
      console.log('✅ WebSocket konektovan');
      // Pridruži se privatnoj sobi za ovog korisnika
      this.socket?.emit('join_user_room', { user_id: this.userId });
    });

    this.socket.on('connection_response', (data) => {
      console.log('📡 Server response:', data.message);
    });

    this.socket.on('room_joined', (data) => {
      console.log('🚪 Pridružio se sobi:', data.room);
    });

    this.socket.on('disconnect', () => {
      console.log('🔴 WebSocket diskonektovan');
    });

    this.socket.on('connect_error', (error) => {
      console.error('❌ WebSocket greška:', error);
    });
  }

  disconnect() {
    if (this.socket) {
      if (this.userId) {
        this.socket.emit('leave_user_room', { user_id: this.userId });
      }
      this.socket.disconnect();
      this.socket = null;
      this.userId = null;
      console.log('🔴 WebSocket diskonektovan');
    }
  }

  // Slušaj promenu uloge
  onRoleChanged(callback: (data: { user_id: number; new_role: string; message: string }) => void) {
    this.socket?.on('role_changed', callback);
  }


  // Ukloni event listener
  off(eventName: string) {
    this.socket?.off(eventName);
  }

  isConnected(): boolean {
    return this.socket?.connected || false;
  }
}

export default new WebSocketService();