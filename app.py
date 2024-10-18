from flask import Flask
from flask_cors import CORS, cross_origin
from flask_jwt_extended import JWTManager
from config import Config
from models import db
from auth import auth
from todos import todos

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    # eventually need to make it only allowed from the front url
    CORS(app, resources={r"/*": {"origins": "*"}})

    JWTManager(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()  # Create database tables

    # Register blueprints
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(todos, url_prefix='/todos')

    @app.route('/')
    @cross_origin()
    def index():
        return 'API is running...'

    return app

def getApp():
    return app

# if __name__ == '__main__':
#     app = create_app()
#     app.run(port=5000, debug=True)
