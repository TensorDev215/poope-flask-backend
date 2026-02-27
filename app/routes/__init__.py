from .auth import auth_bp
from .cache import cache_bp
from .transaction import transaction_bp
from .upload import upload_bp
from .user import user_bp
from . import socket

def init_routes(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(cache_bp)
    app.register_blueprint(transaction_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(user_bp)
