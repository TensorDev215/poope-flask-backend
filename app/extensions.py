from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy

socketio = SocketIO(cors_allowed_origins="http://localhost:8080")
jwt = JWTManager()
cache = Cache()
db = SQLAlchemy()

def init_extensions(app):
    db.init_app(app)
    socketio.init_app(app)
    jwt.init_app(app)
    cache.init_app(app)

    

    # app.config['JWT_TOKEN_LOCATION'] = ['headers']
    # app.config['JWT_HEADER_NAME'] = 'Authorization'
    # app.config['JWT_HEADER_TYPE'] = 'Bearer'



    
