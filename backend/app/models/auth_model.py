import re
from datetime import datetime, timedelta

import bcrypt
import jwt
import psycopg2
from flask import jsonify

from app.config.config import config
from app.database.database import Database


class auth_model:
    def __init__(self):
        self.db = Database()

    @staticmethod
    def validate_email(email):
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(email_regex, email) is not None

    @staticmethod
    def validate_password(password):
        password_regex = (
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        )
        return re.match(password_regex, password) is not None

    def user_exists(self, email):
        """Check if the user already exists in the database."""

        query = "SELECT user_id FROM users WHERE email = %s;"
        conn = self.db.is_connected()
        if conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (email,))
                return cursor.fetchone() is not None  # Returns True if user exists
        return False

    def generate_token(self, user_id):
        """Generate a JWT token for authentication."""
        payload = {
            "user_id": str(user_id),
            "exp": datetime.today() + timedelta(hours=12),
        }
        return jwt.encode(payload, config.SECRET_KEY, algorithm="HS256")

    def signup(self, username, email, password):
        """Sign up a new user."""
        if not self.validate_email(email):
            return jsonify({"error": "Invalid email format"}), 400

        if not self.validate_password(password):
            return jsonify({
                "error": "Password must be at least 8 characters, include one uppercase, one lowercase, one number, and one special character"
            }), 400

        if self.user_exists(email):
            return jsonify({"error": "User already exists"}), 400

        password_hash = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

        query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s) RETURNING user_id;"
        conn = self.db.is_connected()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute(query, (username, email, password_hash))
                    user = cursor.fetchone()

                    if not user:
                        return jsonify({"error": "User creation failed"}), 500

                    user_id = user["user_id"]

                    conn.commit()

                    token = self.generate_token(user_id)

                    return jsonify({
                        "message": "User created",
                        "user_id": user_id,
                        "token": token,
                    }), 201

            except psycopg2.Error:
                return jsonify({"error": "Database error"}), 500

        return jsonify({"error": "Database connection failed"}), 500

    def login(self, email, password):
        """Login an existing user."""
        if not self.validate_email(email):
            return jsonify({"error": "Invalid email format"}), 400

        if not self.validate_password(password):
            return jsonify({"error": "Invalid password"}), 400

        if not self.user_exists(email):
            return jsonify({"error": "User doesn't exist"}), 400

        query = "SELECT user_id, password FROM users WHERE email = %s;"
        conn = self.db.is_connected()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute(query, (email,))
                    user = cursor.fetchone()

                if not user:
                    return jsonify({"error": "User doesn't exists"}), 401

                password_hash = user["password"].encode("utf-8")
                if not bcrypt.checkpw(password.encode("utf-8"), password_hash):
                    return jsonify({"error": "Invalid Password"}), 401

                token = self.generate_token(user["user_id"])

                return jsonify({
                    "message": "Login successful",
                    "user_id": user["user_id"],
                    "token": token,
                }), 200

            except psycopg2.Error:
                return jsonify({"error": "Database error"}), 500

        return jsonify({"error": "Database connection failed"}), 500

    def verify_token(self, token):
        try:
            payload = jwt.decode(token, config.SECRET_KEY, algorithms=["HS256"])

            if payload["exp"] < datetime.today().timestamp():
                return jsonify({"error": "Token has expired"}), 401

            return (
                jsonify({"message": "Token is valid", "user_id": payload["user_id"]}),
                200,
            )

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401

        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
