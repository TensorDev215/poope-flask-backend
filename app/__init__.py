from flask import Flask
from flask_cors import CORS
from app.config import Config
import os
from app.extensions import init_extensions
from app.routes import init_routes

def create_app():
    app = Flask(__name__, static_folder='static')
    app.config.from_object(Config)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    CORS(app, origins="http://localhost:8080")
    init_extensions(app)

    init_routes(app)
    
    return app

