from flask import Blueprint, request, jsonify
from Services.AuthService import AuthService
from Domain.services.IAuthService import IAuthService

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

auth_service: IAuthService = AuthService()  

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    token, error = auth_service.login(data.get("email"), data.get("password"))

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