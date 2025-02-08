from flask import Blueprint, jsonify, request
from app.models.auth_model import auth_model


"""
Blueprints in Flask help organize and modularize routes in large applications. 
Instead of defining all routes in one file (app.py), 
we use Blueprints to split routes into separate files and register them in the main app.
"""

auth_route = Blueprint("auth_route", "__main__")
auth_model = auth_model()


@auth_route.route("/api/auth/signup", methods=["POST"])
def signup():
    requested_data = request.get_json()
    username = requested_data.get("username")
    email = requested_data.get("email")
    password = requested_data.get("password")

    if not all([username, email, password]):
        return jsonify({"error": "All fields are required"}), 400

    return auth_model.signup(username, email, password)


@auth_route.route("/api/auth/login", methods=["POST"])
def login():
    requested_data = request.get_json()
    email = requested_data.get("email")
    password = requested_data.get("password")

    if not all([email, password]):
        return jsonify({"error": "Both email and password are required"}), 400

    return auth_model.login(email, password)


@auth_route.route("/api/verify-token", methods=["GET"])
def verify_token():
    """Verify if the JWT token is still valid."""
    token = request.headers.get("x-auth-token")

    if not token:
        return jsonify({"error": "Token is missing"}), 403

    return auth_model.verify_token(token)
