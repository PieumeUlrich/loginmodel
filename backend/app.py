from flask import Flask
from flask_restx import Api
from models import User
from exts import db
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_cors import CORS
from user import user
from auth import auth

def create_app(config):

    app = Flask(__name__)
    app.config.from_object(config)
    CORS(app)
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    JWTManager(app)


    @app.shell_context_processor
    def make_shell_context():
        return {
            "db": db,
            "User": User
            }
    with app.app_context():
        # Imports
        api = Api(app, doc='/menu')
        api.add_namespace(user)
        api.add_namespace(auth)

        db.create_all()
        return app