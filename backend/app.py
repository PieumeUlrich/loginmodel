from flask import Flask, request
from flask_pymongo import PyMongo
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
    mongodb_client = PyMongo(app)
    dbMongo = mongodb_client.db
    # db = SQLAlchemy()
    # db.init_app(app)
    JWTManager(app)
    login_manager = LoginManager()
    login_manager.init_app(app)



    @app.errorhandler(404)
    def not_found(error=None):
        message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
        }

        return message, 404

    # @app.shell_context_processor
    # def make_shell_context():
    #     return {
    #         "db": db,
    #         "User": User
    #         }
    with app.app_context():
        app.register_blueprint(user)
        app.register_blueprint(auth)
        # Imports
        # api = Api(app, doc='/menu')
        # api.add_namespace(user)
        # api.add_namespace(auth)

        # db.create_all()
        return app