from datetime import datetime
from functools import wraps

import jwt
from flask import jsonify, request

from app.config.config import config


def token_required(f):
    """Middleware to protect routes by requiring a valid JWT token."""
    @wraps(f)
    def decorated_func(*args, **kwargs):
        token = request.headers.get("x-auth-token")

        if not token:
            return jsonify({"error": "Token is missing (Forbidden)"}), 403

        try:
            payload = jwt.decode(token, config.SECRET_KEY, algorithms=["HS256"])

            if payload["exp"] < datetime.today().timestamp():
                return jsonify({"error": "Token has expired (Unauthorized)"}), 401

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401

        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)

    return decorated_func
