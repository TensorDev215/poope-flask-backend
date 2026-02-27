from app import create_app
from app.extensions import db, socketio
from flask_migrate import Migrate

app = create_app()
migrate = Migrate(app, db)

if __name__ == '__main__':
    socketio.run(app, debug=True)