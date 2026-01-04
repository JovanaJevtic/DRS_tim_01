from functools import wraps
from flask import request, jsonify
import jwt
import os

JWT_SECRET = os.getenv("JWT_SECRET")

def authenticate(fn):
    """Middleware za proveru JWT tokena"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"success": False, "message": "Nedostaje token"}), 401

        token = auth_header.split(" ")[1]

        try:
            decoded = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            request.user = decoded  # Dodaj user podatke u request
            return fn(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify({"success": False, "message": "Token je istekao"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"success": False, "message": "Nevažeći token"}), 401

    return wrapper