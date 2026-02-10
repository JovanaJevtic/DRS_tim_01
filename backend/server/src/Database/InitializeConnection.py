from flask import Flask
from Database.DbConnectionPool import db
import os

def initialize_connection(app: Flask):
    ENV = os.getenv("APP_ENV", "local")

    DB_HOST = (
        os.getenv("DB_HOST_DOCKER")
        if ENV == "docker"
        else os.getenv("DB_HOST_LOCAL")
    )

    DB_PORT = int(os.getenv("DB_PORT", "3306"))

    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{DB_HOST}:{DB_PORT}/{os.getenv('DB_NAME')}"
    )

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()
        print("\x1b[34m[AuditDB@1.0.0]\x1b[0m Database connected")
