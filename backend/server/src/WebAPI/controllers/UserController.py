from flask import Blueprint, request, jsonify, send_from_directory
from Domain.services.IUserService import IUserService
from Middlewares.authentification.AuthMiddleware import authenticate
from Middlewares.authorization.AuthorizeMiddleware import authorize
from Domain.models.User import User
from Domain.enums.Uloga import UlogaEnum
from Database.DbConnectionPool import db
from Domain.enums.Pol import PolEnum
from datetime import datetime
import os
import time
from werkzeug.utils import secure_filename
from Services.EmailService import EmailService
from WebSocket.Events import emit_role_changed

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def create_user_controller(user_service: IUserService):
    user_bp = Blueprint("user_controller", __name__)
    
    email_service = EmailService()

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
        
        # Promeni ulogu
        user.uloga = UlogaEnum(new_role)
        db.session.commit()
        
        # Pošalji email
        user_name = f"{user.ime} {user.prezime}" if user.ime and user.prezime else user.email
        email_sent = email_service.send_role_change_email(
            user_email=user.email,
            user_name=user_name,
            new_role=new_role
        )
        
        if email_sent:
            print(f"✅ Email o promeni uloge poslat korisniku: {user.email}")
        else:
            print(f"⚠️ Email nije poslat, ali uloga je promenjena")
        
        # Emituj WebSocket event
        emit_role_changed(user_id, new_role)
        
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
    @user_bp.route("/users/me", methods=["GET"])
    @authenticate
    def get_my_profile():
        """Dohvati podatke trenutnog korisnika"""
        user_id = request.user["id"]
        user = db.session.get(User, user_id)
        
        if not user:
            return jsonify({"success": False, "message": "Korisnik ne postoji"}), 404
        
        # Pripremi URL slike ako postoji
        profile_image_url = None
        if user.profile_image:
            profile_image_url = f"/api/v1/uploads/{user.profile_image}"
        
        user_data = {
            "id": user.id,
            "ime": user.ime,
            "prezime": user.prezime,
            "email": user.email,
            "datum_rodjenja": user.datum_rodjenja.isoformat() if user.datum_rodjenja else None,
            "pol": user.pol.value if user.pol else None,
            "drzava": user.drzava,
            "ulica": user.ulica,
            "broj": user.broj,
            "uloga": user.uloga.value,
            "profile_image": profile_image_url
        }
        
        return jsonify({"success": True, "user": user_data}), 200

    @user_bp.route("/users/me", methods=["PUT"])
    @authenticate
    def update_my_profile():
        data = request.json
        user_id = request.user["id"]

        user = db.session.get(User, user_id)
        if not user:
            return jsonify({"success": False, "message": "Korisnik ne postoji"}), 404

        # Polja za izmenu - ignoriši prazne stringove
        if "ime" in data and data["ime"]:
            user.ime = data["ime"]
        
        if "prezime" in data and data["prezime"]:
            user.prezime = data["prezime"]
        
        if "datum_rodjenja" in data and data["datum_rodjenja"]:
            try:
                user.datum_rodjenja = datetime.strptime(data["datum_rodjenja"], "%Y-%m-%d").date()
            except ValueError:
                return jsonify({"success": False, "message": "Neispravan format datuma"}), 400
        
        if "pol" in data and data["pol"]:
            pol_map = {"M": PolEnum.MUSKI, "Z": PolEnum.ZENSKI, "O": PolEnum.DRUGO}
            pol = pol_map.get(data["pol"].upper())
            if not pol:
                return jsonify({"success": False, "message": "Neispravan pol"}), 400
            user.pol = pol
        
        if "drzava" in data and data["drzava"]:
            user.drzava = data["drzava"]
        
        if "ulica" in data and data["ulica"]:
            user.ulica = data["ulica"]
        
        if "broj" in data and data["broj"]:
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

        # PROVERA FORMATA
        if not allowed_file(file.filename):
            return jsonify({"success": False, "message": "Nepodržan tip fajla. Dozvoljeni: PNG, JPG, JPEG, GIF"}), 400

        # PROVERA VELIČINE (5MB)
        file.seek(0, os.SEEK_END)
        file_length = file.tell()
        file.seek(0)  # Vrati na početak
        
        if file_length > MAX_FILE_SIZE:
            size_mb = file_length / (1024 * 1024)
            return jsonify({"success": False, "message": f"Fajl je prevelik ({size_mb:.1f}MB). Maksimalna veličina: 5MB"}), 400

        # SAČUVAJ FAJL sa jedinstvenim imenom
        filename = secure_filename(file.filename)
        unique_filename = f"{int(time.time())}_{filename}"
        upload_path = os.path.join(UPLOAD_FOLDER, unique_filename)

        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        file.save(upload_path)

        # AŽURIRAJ KORISNIKA U BAZI
        user_id = request.user["id"]
        user = db.session.get(User, user_id)
        user.profile_image = unique_filename  # Čuvaj samo ime fajla
        db.session.commit()

        # VRATI URL SLIKE
        image_url = f"/api/v1/uploads/{unique_filename}"
        return jsonify({"success": True, "profile_image": image_url}), 200

    return user_bp