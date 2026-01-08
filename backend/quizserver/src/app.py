
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

from flask import Flask
from flask_cors import CORS
from flask_mail import Mail
import os

from Database.MongoConnection import MongoConnection
from WebAPI.controllers.QuizController import quiz_bp

def create_app():
    app = Flask(__name__)

    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": [
                    "http://localhost:5173",  # frontend (Vite)
                    "http://localhost:5000",  # auth/server
                ],
                "methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization"],
            }
        },
    )


    print(" .env path:", env_path)
    print(" .env exists:", env_path.exists())
    print("📧 MAIL_USERNAME:", os.getenv("MAIL_USERNAME"))
    print("📧 MAIL_DEFAULT_SENDER:", os.getenv("MAIL_DEFAULT_SENDER"))

    app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT", 587))
    app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS", "True") == "True"
    app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
    app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")

    # Inicijalizuj Mail
    Mail(app)

    MongoConnection.initialize()

    app.register_blueprint(quiz_bp, url_prefix="/api/v1")


    @app.route("/health", methods=["GET"])
    def health_check():
        return {
            "status": "ok",
            "service": "Quiz Service",
        }, 200

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5001)),
        debug=True,
    )
