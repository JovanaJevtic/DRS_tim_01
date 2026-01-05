from flask import Flask
from flask_cors import CORS
from flask_mail import Mail
from dotenv import load_dotenv
import os
from pathlib import Path
from Database.MongoConnection import MongoConnection
from WebAPI.controllers.QuizController import quiz_bp

env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

def create_app():
    app = Flask(__name__)
    
    # CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:5173", "http://localhost:5000"],
            "methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # DEBUG - proveri da li .env učitava
    print(f"🔍 .env path: {env_path}")
    print(f"🔍 .env exists: {env_path.exists()}")
    print(f"🔍 MAIL_USERNAME: {os.getenv('MAIL_USERNAME')}")
    print(f"🔍 MAIL_DEFAULT_SENDER: {os.getenv('MAIL_DEFAULT_SENDER')}")
    
    # Email konfiguracija
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', 'kvizplatforma@gmail.com')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', 'kvizplatforma123')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', 'kvizplatforma@gmail.com')
    
    # Inicijalizuj Mail
    mail = Mail(app)
    
    # Inicijalizuj MongoDB
    MongoConnection.initialize()
    
    # Registruj QuizController
    app.register_blueprint(quiz_bp, url_prefix="/api/v1")
    
    @app.route("/health", methods=["GET"])
    def health_check():
        return {"status": "ok", "service": "Quiz Service"}, 200
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5001)),
        debug=True
    )