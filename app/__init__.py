from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
from .routes import main

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    app.register_blueprint(main)

    return app

