from flask import Blueprint, request, jsonify
from Services.AuthService import AuthService
from Domain.services.IAuthService import IAuthService

auth_bp = Blueprint("auth", __name__)

auth_service: IAuthService = AuthService()  

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "success": False,
            "message": "Invalid or missing JSON body"
        }), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "success": False,
            "message": "Email and password are required"
        }), 400

    token, error = auth_service.login(email, password)

    if error:
        return jsonify({"success": False, "message": error}), 401

    return jsonify({"success": True, "token": token}), 200


@auth_bp.route("/register", methods=["POST"]) 
def register():
    data = request.json
    user, error = auth_service.register(data)
    if error:
        return jsonify({"success": False, "message": error}), 400
    return jsonify({"success": True, "user_id": user.id}), 201