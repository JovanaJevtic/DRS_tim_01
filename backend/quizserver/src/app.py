from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os
from Database.MongoConnection import MongoConnection
from WebAPI.controllers.QuizController import quiz_bp

load_dotenv()

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