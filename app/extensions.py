from .models import db
from flask_jwt_extended import JWTManager

def init_extensions(app):
    db.init_app(app)

    jwt = JWTManager(app)



    
