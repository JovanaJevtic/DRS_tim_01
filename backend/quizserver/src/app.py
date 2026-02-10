from dotenv import load_dotenv
from Services.RedisService import RedisService  
from pathlib import Path
from flask import Flask
from flask_cors import CORS
from Services.EmailService import mail
import os
import atexit
import signal
from Database.MongoConnection import MongoConnection
from WebAPI.controllers.QuizController import quiz_bp

BASE_DIR = Path(__file__).resolve().parent.parent

ENV = os.getenv("APP_ENV", "local")

if ENV == "docker":
    print("🐳 QuizServer running in DOCKER mode")
    load_dotenv(BASE_DIR / ".env.docker", override=True)
else:
    print("💻 QuizServer running in LOCAL mode")
    load_dotenv(BASE_DIR / ".env.local", override=True)

JWT_SECRET = os.getenv("JWT_SECRET")

if not JWT_SECRET:
    raise RuntimeError("❌ JWT_SECRET is NOT loaded!")

def create_app():
    app = Flask(__name__)

    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": [
                    "http://localhost:5173",
                    "http://localhost:3000",  
                    "http://localhost:5000",
                ],
                "methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization"],
            }
        },
    )


    print("📧 MAIL_USERNAME:", os.getenv("MAIL_USERNAME"))
    print("📧 MAIL_DEFAULT_SENDER:", os.getenv("MAIL_DEFAULT_SENDER"))

    app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT", 587))
    app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS", "True") == "True"
    app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
    app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")

    mail.init_app(app)
    MongoConnection.initialize()
    RedisService.initialize()

    app.register_blueprint(quiz_bp, url_prefix="/api/v1")

    @app.route("/health", methods=["GET"])
    def health_check():
        from Services.ProcessPoolService import ProcessPoolService
        pool_info = ProcessPoolService.get_pool_info()
        return {
            "status": "ok",
            "service": "Quiz Service",
            "process_pool": pool_info
        }, 200
    
    def cleanup():
        """Cleanup funkcija koja se poziva pri gašenju servera"""
        from Services.ProcessPoolService import ProcessPoolService
        print("\n Shutting down Quiz Service...")
        ProcessPoolService.close()
        MongoConnection.close()
        print("👋 Goodbye!")
    
    atexit.register(cleanup)
    
    def signal_handler(sig, frame):
        print(f"\n Received signal {sig}")
        cleanup()
        exit(0)
    
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    return app


if __name__ == "__main__":
    from multiprocessing import freeze_support
    freeze_support()
    
    app = create_app()
    print("\n" + "="*60)
    print(" Quiz Service pokrenut sa PROCESS POOL podrškom!")
    print(" Asinhrona obrada kvizova omogućena!")
    print(" Asinhrono generisanje PDF izvještaja omogućeno!")
    print("="*60 + "\n")
    
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5001)),
        debug=True,
        use_reloader=False 
    )