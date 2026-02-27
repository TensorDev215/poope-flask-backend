import os

class Config:
    SECRET_KEY = 'asdfdsfasfasdfasdf'
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:123456789@localhost/poope-db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'jwjjsjjsjsjsdfd'
    JWT_DECODE_AUDIENCE = None
    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFAULT_TIMEOUT = 6000
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static', 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'txt'}
    MAX_CONTENT_LENGTH = 16 * 1000 * 1000

