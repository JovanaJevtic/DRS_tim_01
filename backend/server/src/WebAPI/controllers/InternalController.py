from flask import Blueprint, request, jsonify
from WebSocket.SocketConfig import socketio

internal_bp = Blueprint("internal", __name__)

@internal_bp.route("/internal/quiz/created", methods=["POST"])
def quiz_created():
    """Primi notifikaciju da je kviz kreiran i emituj WebSocket event"""
    try:
        quiz_data = request.json
        
        print(f" Primljena notifikacija o novom kvizu: {quiz_data.get('naziv')}")
        
        # Emituj WebSocket event ka SVIM korisnicima (Admin će ga čuti)
        socketio.emit('new_quiz_created', {
            'quiz_id': quiz_data.get('id'),
            'naziv': quiz_data.get('naziv'),
            'autor_email': quiz_data.get('autor_email'),
            'autor_id': quiz_data.get('autor_id'),
            'message': f"Novi kviz '{quiz_data.get('naziv')}' čeka odobrenje!"
        })
        
        print(f" WebSocket event 'new_quiz_created' emitovan")
        
        return jsonify({"success": True, "message": "Notifikacija primljena"}), 200
        
    except Exception as e:
        print(f" Greška u internal/quiz/created: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 500


@internal_bp.route("/internal/quiz/approved", methods=["POST"])
def quiz_approved():
    """Primi notifikaciju da je kviz odobren"""
    try:
        data = request.json
        quiz_id = data.get('quiz_id')
        moderator_id = data.get('moderator_id')
        
        print(f" Kviz {quiz_id} odobren, obaveštavam moderatora {moderator_id}")
        
        # Emituj WebSocket event ka moderatoru
        socketio.emit('quiz_approved', {
            'quiz_id': quiz_id,
            'message': 'Vaš kviz je odobren i sada je vidljiv igračima!'
        }, room=f"user_{moderator_id}")
        
        print(f" WebSocket event 'quiz_approved' emitovan")
        
        return jsonify({"success": True}), 200
        
    except Exception as e:
        print(f" Greška: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 500


@internal_bp.route("/internal/quiz/rejected", methods=["POST"])
def quiz_rejected():
    """Primi notifikaciju da je kviz odbijen"""
    try:
        data = request.json
        quiz_id = data.get('quiz_id')
        razlog = data.get('razlog')
        moderator_id = data.get('moderator_id')
        
        print(f" Kviz {quiz_id} odbijen, obaveštavam moderatora {moderator_id}")
        
        socketio.emit('quiz_rejected', {
            'quiz_id': quiz_id,
            'razlog': razlog,
            'message': f'Vaš kviz je odbijen. Razlog: {razlog}'
        }, room=f"user_{moderator_id}")
        
        print(f" WebSocket event 'quiz_rejected' emitovan")
        
        return jsonify({"success": True}), 200
        
    except Exception as e:
        print(f" Greška: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 500