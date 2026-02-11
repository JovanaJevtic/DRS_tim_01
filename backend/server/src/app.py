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
from WebSocket.SocketConfig import init_socketio, socketio
import WebSocket.Events
from WebAPI.controllers.InternalController import internal_bp

load_dotenv()

ENV = os.getenv("APP_ENV", "local")

DB_HOST = (
    os.getenv("DB_HOST_DOCKER")
    if ENV == "docker"
    else os.getenv("DB_HOST_LOCAL")
)

DB_PORT = int(os.getenv("DB_PORT"))


def create_app():
    app = Flask(__name__)

    #CORS(app, resources={
    #    r"/api/*": {
    #        "origins": ["http://localhost:3000",
    #                    "http://localhost:5173",
    #                    "http://192.168.24.1:3000"],
    #        "methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    #        "allow_headers": ["Content-Type", "Authorization"]
    #    }
    #})
    CORS(app, supports_credentials=True)

    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')
    
    mail.init_app(app)

    initialize_connection(app)

    socketio.init_app(
        app,
        cors_allowed_origins="*"
    )

    user_service = UserService()
    user_controller = create_user_controller(user_service)

    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
    app.register_blueprint(user_controller, url_prefix="/api/v1")
    app.register_blueprint(internal_bp, url_prefix="/api/v1")
    
    return app


if __name__ == "__main__":
    app = create_app()
    socketio.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)