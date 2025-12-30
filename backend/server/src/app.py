from flask import Flask
from dotenv import load_dotenv
import os
from Database.DbConnectionPool import db
from Database.InitializeConnection import initialize_connection
from WebAPI.controllers.AuthController import auth_bp
from WebAPI.controllers.UserController import create_user_controller
from Services.UserService import UserService

load_dotenv()


def create_app():
    app = Flask(__name__)

    initialize_connection(app)

    user_service = UserService()

    user_controller = create_user_controller(user_service)

    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
    app.register_blueprint(user_controller, url_prefix="/api/v1")

    return app


app = create_app()

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000)),
        debug=True
    )
