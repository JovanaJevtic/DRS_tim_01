from functools import wraps
from flask import request, jsonify
import jwt
import os

def authenticate(fn):
    """Middleware za proveru JWT tokena"""
    @wraps(fn)
    def wrapper(*args, **kwargs):

        if request.method == "OPTIONS":
            return fn(*args, **kwargs)

        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            print("❌ NEMA AUTH HEADERA")
            return jsonify({"success": False, "message": "Nedostaje token"}), 401

        token = auth_header.split(" ")[1]

        JWT_SECRET = os.getenv("JWT_SECRET")

        if not JWT_SECRET:
            print("❌ JWT_SECRET NIJE UČITAN")
            return jsonify({"success": False, "message": "Server configuration error"}), 500

        try:
            decoded = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            print("✅ DECODED TOKEN:", decoded)
            request.user = decoded
            return fn(*args, **kwargs)

        except jwt.ExpiredSignatureError:
            print("⏰ TOKEN EXPIRED")
            return jsonify({"success": False, "message": "Token je istekao"}), 401

        except jwt.InvalidTokenError as e:
            print("❌ INVALID TOKEN:", str(e))
            return jsonify({"success": False, "message": "Nevažeći token"}), 401

    return wrapper
