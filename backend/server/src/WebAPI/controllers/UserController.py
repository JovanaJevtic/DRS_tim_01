from flask import Blueprint, request, jsonify
from Domain.services.IUserService import IUserService
from Middlewares.authentification.AuthMiddleware import authenticate
from Middlewares.authorization.AuthorizeMiddleware import authorize
from Domain.models.User import User
from Domain.enums.Uloga import UlogaEnum
from Database.DbConnectionPool import db

def create_user_controller(user_service: IUserService):
    user_bp = Blueprint("user_controller", __name__)

    @user_bp.route("/users", methods=["GET"])
    @authenticate
    @authorize(UlogaEnum.ADMINISTRATOR.value)
    def get_svi_korisnici():
        try:
            korisnici = user_service.get_svi_korisnici()
            return jsonify([korisnik.__dict__ for korisnik in korisnici]), 200
        except Exception as e:
            return jsonify({"success": False, "message": str(e)}), 500

    @user_bp.route("/users/<int:user_id>/role", methods=["PATCH"])
    @authenticate
    @authorize(UlogaEnum.ADMINISTRATOR.value)
    def change_role(user_id):
        data = request.json
        new_role = data.get("uloga")
        if new_role not in UlogaEnum._value2member_map_:
            return jsonify({"success": False, "message": "Nevalidna uloga"}), 400
        user = db.session.get(User, user_id)
        if not user:
            return jsonify({"success": False, "message": "Korisnik ne postoji"}), 404
        user.uloga = UlogaEnum(new_role)
        db.session.commit()
        return jsonify({"success": True}), 200

    @user_bp.route("/users/<int:user_id>", methods=["DELETE"])
    @authenticate
    @authorize(UlogaEnum.ADMINISTRATOR.value)
    def delete_user(user_id):
        user = db.session.get(User, user_id)
        if not user:
            return jsonify({"success": False, "message": "Korisnik ne postoji"}), 404
        db.session.delete(user)
        db.session.commit()
        return jsonify({"success": True}), 200

    return user_bp
