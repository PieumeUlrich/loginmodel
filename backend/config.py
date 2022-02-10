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
    SECRET_KEY = config('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = config('SQLALCHEMY_TRACK_MODIFICATIONS', cast=bool)


class DevConfig(Config):
    FLASK_ENV = config('FLASK_ENV')
    SQLALCHEMY_DATABASE_URI = "sqlite:///"+path.join(basedir, 'db.sqlite')
    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///"+path.join(basedir, 'prod.sqlite')
    DEBUG = False
    SQLALCHEMY_ECHO = True
