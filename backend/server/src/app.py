from flask import Flask, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import os
from Database.DbConnectionPool import db
from Database.InitializeConnection import initialize_connection
from WebAPI.controllers.AuthController import auth_bp
from WebAPI.controllers.UserController import create_user_controller
from Services.UserService import UserService
from Services.EmailService import mail

load_dotenv()


def create_app():
    app = Flask(__name__)

    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:5173"],
            "methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })

    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')
    
    mail.init_app(app)

    initialize_connection(app)

    user_service = UserService()
    user_controller = create_user_controller(user_service)

    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
    app.register_blueprint(user_controller, url_prefix="/api/v1")

    # APSOLUTNA PUTANJA do uploads foldera
    # Idemo 1 folder gore iz src/ da bi došli do server/, pa u uploads/
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")
    print(f"📁 UPLOAD_FOLDER: {UPLOAD_FOLDER}")  # Debug log
    
    @app.route("/api/v1/uploads/<filename>", methods=["GET"])
    def serve_upload(filename):
        """Serviranje uploaded fajlova"""
        print(f"🖼️ Tražena slika: {filename}")  # Debug log
        print(f"📂 Tražim u: {UPLOAD_FOLDER}")  # Debug log
        try:
            return send_from_directory(UPLOAD_FOLDER, filename)
        except FileNotFoundError:
            print(f"❌ Fajl ne postoji: {os.path.join(UPLOAD_FOLDER, filename)}")
            return {"success": False, "message": "Fajl ne postoji"}, 404

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000)),
        debug=True
    )