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

# ===============================
# ENVIRONMENT LOGIC
# ===============================

ENV = os.getenv("APP_ENV", "local")

if ENV == "local":
    print("💻 QuizServer running in LOCAL mode")
    load_dotenv(BASE_DIR / ".env.local")

elif ENV == "docker":
    print("🐳 QuizServer running in DOCKER mode")
    load_dotenv(BASE_DIR / ".env.docker")

elif ENV == "production":
    print("🚀 QuizServer running in PRODUCTION mode")
    # Production koristi Render environment varijable
    # NE učitavamo .env fajlove

else:
    print(f"⚠️ Unknown APP_ENV: {ENV}")

# ===============================
# SECURITY CHECK
# ===============================

JWT_SECRET = os.getenv("JWT_SECRET")

if not JWT_SECRET:
    raise RuntimeError("❌ JWT_SECRET is NOT loaded!")

# ===============================
# APP FACTORY
# ===============================

def create_app():
    app = Flask(__name__)

    CORS(app, supports_credentials=True)

    print("📧 MAIL_USERNAME:", os.getenv("MAIL_USERNAME"))
    print("📧 MAIL_DEFAULT_SENDER:", os.getenv("MAIL_DEFAULT_SENDER"))

    # Mail konfiguracija
    app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT", 587))
    app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS", "True") == "True"
    app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
    app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")

    mail.init_app(app)

    # Initialize databases
    MongoConnection.initialize()
    RedisService.initialize()

    # Register routes
    app.register_blueprint(quiz_bp, url_prefix="/api/v1")

    # Health check
    @app.route("/health", methods=["GET"])
    def health_check():
        from Services.ProcessPoolService import ProcessPoolService
        pool_info = ProcessPoolService.get_pool_info()
        return {
            "status": "ok",
            "service": "Quiz Service",
            "process_pool": pool_info
        }, 200

    # Cleanup logic
    def cleanup():
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


# ===============================
# LOCAL RUN
# ===============================

if __name__ == "__main__":
    from multiprocessing import freeze_support
    freeze_support()

    app = create_app()

    print("\n" + "=" * 60)
    print(" Quiz Service pokrenut sa PROCESS POOL podrškom!")
    print(" Asinhrona obrada kvizova omogućena!")
    print(" Asinhrono generisanje PDF izvještaja omogućeno!")
    print("=" * 60 + "\n")

    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5001)),
        debug=(ENV == "local"),
        use_reloader=False
    )
