from functools import wraps
from flask import request, jsonify


def authorize(*dozvoljene_uloge):
    """Middleware za proveru uloge korisnika"""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user = getattr(request, "user", None)

            if not user or user.get("uloga") not in dozvoljene_uloge:
                return jsonify({
                    "success": False,
                    "message": "Zabranjen pristup"
                }), 403

            return fn(*args, **kwargs)

        return wrapper
    return decorator