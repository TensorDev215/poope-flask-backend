from app import create_app
from app.extensions import init_extensions, db
from flask_migrate import Migrate

app = create_app()
init_extensions(app)
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(debug=True)