from flask import Flask
from flask_cors import CORS, cross_origin
from flask_jwt_extended import JWTManager
from sqlalchemy import inspect
from models import db
from auth import auth
from todos import todos
from commands import create_tables

def create_app(config_file='config.py'):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)

    # Initialize extensions
    # eventually need to make it only allowed from the front url
    CORS(app, resources={r"/*": {"origins": "*"}})

    JWTManager(app)
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(todos, url_prefix='/todos')

    @app.route('/')
    def index():
        return "<h1> Deployed to Heroku</h1>"

    app.cli.add_command(create_tables)

    return app

# if __name__ == '__main__':
#     app = create_app()
#     app.run(port=5000, debug=True)
