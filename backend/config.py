"""Flask app configuration."""
from typing import ClassVar
from decouple import config
from os import environ, path

basedir = path.dirname(path.realpath(__file__))
# load_dotenv(path.join(basedir, '.env'))


class Config:
    """Set Flask configuration from environment variables."""

    FLASK_APP = 'run.py'

    # # Flask-Assets
    # LESS_BIN = environ.get('LESS_BIN')
    # ASSETS_DEBUG = environ.get('ASSETS_DEBUG')
    # LESS_RUN_IN_DEBUG = environ.get('LESS_RUN_IN_DEBUG')

    # # Flask-SQLAlchemy
    SECRET_KEY = 'eb7852eb33c349v89995349d'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    FLASK_ENV = config('FLASK_ENV')
    SQLALCHEMY_DATABASE_URI = "sqlite:///"+path.join(basedir, 'db.sqlite')
    MONGO_URI=''
    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///"+path.join(basedir, 'prod.sqlite')
    MONGO_URI=''
    DEBUG = False
    SQLALCHEMY_ECHO = True
