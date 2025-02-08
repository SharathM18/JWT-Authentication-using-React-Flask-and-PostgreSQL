from flask import Flask
from flask_cors import CORS

from .api.auth_routes import auth_route


def create_app():
    app = Flask(__name__)
    CORS(app)

    # Register API routes
    app.register_blueprint(auth_route)

    return app

