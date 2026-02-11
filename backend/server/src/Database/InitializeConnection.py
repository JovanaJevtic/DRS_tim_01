from flask import Flask
from Database.DbConnectionPool import db
import os

def initialize_connection(app: Flask):

    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise RuntimeError("❌ DATABASE_URL is not set!")

    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()
        print("\x1b[34m[AuditDB@1.0.0]\x1b[0m Database connected")
