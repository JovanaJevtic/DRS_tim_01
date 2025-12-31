from flask import Blueprint, request, jsonify
from Domain.services.IUserService import IUserService
from Middlewares.authentification.AuthMiddleware import authenticate
from Middlewares.authorization.AuthorizeMiddleware import authorize
from Domain.models.User import User
from Domain.enums.Uloga import UlogaEnum
from Database.DbConnectionPool import db
from Domain.enums.Pol import PolEnum
from datetime import datetime
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def create_user_controller(user_service: IUserService):
    user_bp = Blueprint("user_controller", __name__)

    # -------------------- ADMIN ENDPOINTS --------------------
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

    # -------------------- USER ENDPOINTS --------------------
    @user_bp.route("/users/me", methods=["PUT"])
    @authenticate
    def update_my_profile():
        data = request.json
        user_id = request.user["id"]

        user = db.session.get(User, user_id)
        if not user:
            return jsonify({"success": False, "message": "Korisnik ne postoji"}), 404

        # Polja za izmjenu
        if "ime" in data:
            user.ime = data["ime"]
        if "prezime" in data:
            user.prezime = data["prezime"]
        if "datum_rodjenja" in data:
            user.datum_rodjenja = datetime.strptime(data["datum_rodjenja"], "%Y-%m-%d").date()
        if "pol" in data:
            pol_map = {"M": PolEnum.MUSKI, "Z": PolEnum.ZENSKI, "O": PolEnum.DRUGO}
            pol = pol_map.get(data["pol"].upper())
            if not pol:
                return jsonify({"success": False, "message": "Neispravan pol"}), 400
            user.pol = pol
        if "drzava" in data:
            user.drzava = data["drzava"]
        if "ulica" in data:
            user.ulica = data["ulica"]
        if "broj" in data:
            user.broj = data["broj"]

        db.session.commit()
        return jsonify({"success": True, "message": "Profil ažuriran"}), 200

    @user_bp.route("/users/me/avatar", methods=["POST"])
    @authenticate
    def upload_avatar():
        if "file" not in request.files:
            return jsonify({"success": False, "message": "Nema fajla u requestu"}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"success": False, "message": "Fajl nema ime"}), 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_path = os.path.join(UPLOAD_FOLDER, filename)

            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            file.save(upload_path)

            user_id = request.user["id"]
            user = db.session.get(User, user_id)
            user.profile_image = upload_path
            db.session.commit()

            return jsonify({"success": True, "profile_image": upload_path}), 200
        else:
            return jsonify({"success": False, "message": "Nepodržan tip fajla"}), 400

    return user_bp
