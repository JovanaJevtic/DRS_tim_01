from flask import Blueprint, request, jsonify
from Services.QuizService import QuizService
from Domain.services.IServerCommunicationService import IServerCommunicationService
from Services.ServerCommunicationService import ServerCommunicationService
from Domain.services.IQuizService import IQuizService
from WebAPI.validators.QuizValidator import QuizValidator
from Middlewares.authentification.AuthMiddleware import authenticate
from Middlewares.authorization.AuthorizeMiddleware import authorize


quiz_bp = Blueprint("quiz_controller", __name__)

quiz_service: IQuizService = QuizService()
server_comm: IServerCommunicationService = ServerCommunicationService()

# -------------------- ENDPOINTS --------------------

@quiz_bp.route("/quiz/create", methods=["POST"])
@authenticate
@authorize("MODERATOR", "ADMINISTRATOR")
def create_quiz():
    """Kreira novi kviz (samo MODERATOR i ADMIN)"""
    try:
        data = request.json
        
        # VALIDACIJA
        is_valid, error_msg = QuizValidator.validate_create_quiz(data)
        if not is_valid:
            return jsonify({"success": False, "message": error_msg}), 400
        
        # Dodaj podatke o autoru iz JWT tokena
        data["autor_id"] = request.user["id"]
        data["autor_email"] = request.user["email"]
        
        # Kreiraj kviz
        quiz, error = quiz_service.create_quiz(data)
        
        if error:
            return jsonify({"success": False, "message": error}), 400
        
        # OBAVESTI SERVER - WebSocket notifikacija adminu
        server_comm.notify_new_quiz(quiz)
        
        return jsonify({"success": True, "quiz": quiz}), 201
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@quiz_bp.route("/quiz/all", methods=["GET"])
@authenticate
def get_all_quizzes():
    """Dohvata sve kvizove - filtriranje po ulozi"""
    try:
        user_role = request.user.get("uloga")
        
        # ADMIN vidi SVE kvizove
        if user_role == "ADMINISTRATOR":
            status_filter = request.args.get("status")
            quizzes = quiz_service.get_all_quizzes(status=status_filter)
        
        # MODERATOR vidi svoje kvizove
        elif user_role == "MODERATOR":
            all_quizzes = quiz_service.get_all_quizzes()
            autor_id = request.user["id"]
            quizzes = [q for q in all_quizzes if q["autor_id"] == autor_id]
        
        # IGRAČ vidi samo APPROVED kvizove
        else:
            quizzes = quiz_service.get_all_quizzes(status="APPROVED")
        
        return jsonify({"success": True, "quizzes": quizzes}), 200
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@quiz_bp.route("/quiz/<quiz_id>", methods=["GET"])
@authenticate
def get_quiz_by_id(quiz_id):
    """Dohvata kviz po ID-u"""
    try:
        quiz = quiz_service.get_quiz_by_id(quiz_id)
        
        if not quiz:
            return jsonify({"success": False, "message": "Kviz nije pronađen"}), 404
        
        user_role = request.user.get("uloga")
        
        # ADMIN vidi sve
        if user_role == "ADMINISTRATOR":
            pass
        
        # MODERATOR vidi samo svoje kvizove
        elif user_role == "MODERATOR":
            if quiz["autor_id"] != request.user["id"]:
                return jsonify({"success": False, "message": "Zabranjen pristup"}), 403
        
        # IGRAČ vidi samo APPROVED kvizove
        else:
            if quiz["status"] != "APPROVED":
                return jsonify({"success": False, "message": "Kviz nije dostupan"}), 403
        
        return jsonify({"success": True, "quiz": quiz}), 200
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@quiz_bp.route("/quiz/<quiz_id>/approve", methods=["PATCH"])
@authenticate
@authorize("ADMINISTRATOR")
def approve_quiz(quiz_id):
    """Odobrava kviz (samo ADMIN)"""
    try:
        # Prvo dohvati kviz da znaš ko je autor
        quiz = quiz_service.get_quiz_by_id(quiz_id)
        if not quiz:
            return jsonify({"success": False, "message": "Kviz nije pronađen"}), 404
        
        # Odobri kviz
        success, error = quiz_service.approve_quiz(quiz_id)
        
        if not success:
            return jsonify({"success": False, "message": error}), 400
        
        # OBAVESTI SERVER - moderator će dobiti notifikaciju
        server_comm.notify_quiz_approved(quiz_id, quiz['autor_id'])
        
        return jsonify({"success": True, "message": "Kviz odobren"}), 200
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@quiz_bp.route("/quiz/<quiz_id>/reject", methods=["PATCH"])
@authenticate
@authorize("ADMINISTRATOR")
def reject_quiz(quiz_id):
    """Odbija kviz sa razlogom (samo ADMIN)"""
    try:
        data = request.json
        razlog = data.get("razlog")
        
        if not razlog:
            return jsonify({"success": False, "message": "Razlog odbijanja je obavezan"}), 400
        
        # Prvo dohvati kviz da znaš ko je autor
        quiz = quiz_service.get_quiz_by_id(quiz_id)
        if not quiz:
            return jsonify({"success": False, "message": "Kviz nije pronađen"}), 404
        
        # Odbij kviz
        success, error = quiz_service.reject_quiz(quiz_id, razlog)
        
        if not success:
            return jsonify({"success": False, "message": error}), 400
        
        # OBAVESTI SERVER - moderator će dobiti notifikaciju
        server_comm.notify_quiz_rejected(quiz_id, razlog, quiz['autor_id'])
        
        return jsonify({"success": True, "message": "Kviz odbijen"}), 200
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@quiz_bp.route("/quiz/<quiz_id>", methods=["DELETE"])
@authenticate
@authorize("MODERATOR", "ADMINISTRATOR")
def delete_quiz(quiz_id):
    """Briše kviz (MODERATOR ili ADMIN)"""
    try:
        # Ako je MODERATOR, proveri da li je on autor
        if request.user.get("uloga") == "MODERATOR":
            quiz = quiz_service.get_quiz_by_id(quiz_id)
            if not quiz or quiz["autor_id"] != request.user["id"]:
                return jsonify({"success": False, "message": "Zabranjen pristup"}), 403
        
        success, error = quiz_service.delete_quiz(quiz_id)
        
        if not success:
            return jsonify({"success": False, "message": error}), 400
        
        return jsonify({"success": True, "message": "Kviz obrisan"}), 200
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@quiz_bp.route("/quiz/<quiz_id>/submit", methods=["POST"])
@authenticate
@authorize("IGRAC", "MODERATOR", "ADMINISTRATOR")
def submit_quiz(quiz_id):
    """Igrač šalje odgovore nakon završetka kviza"""
    try:
        data = request.json
        
        # Dodaj podatke o igraču
        data["quiz_id"] = quiz_id
        data["igrac_id"] = request.user["id"]
        data["igrac_email"] = request.user["email"]
        
        result, error = quiz_service.process_quiz_submission(data)
        
        if error:
            return jsonify({"success": False, "message": error}), 400
        
        return jsonify({
            "success": True, 
            "message": "Odgovori primljeni. Rezultati će biti poslati na email.",
            "result": result
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@quiz_bp.route("/quiz/<quiz_id>/leaderboard", methods=["GET"])
@authenticate
def get_leaderboard(quiz_id):
    """Dohvata rang listu za kviz"""
    try:
        leaderboard = quiz_service.get_leaderboard(quiz_id)
        
        return jsonify({"success": True, "leaderboard": leaderboard}), 200
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500