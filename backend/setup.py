from flask import Flask
from models import setup_db

from flask_bcrypt import Bcrypt
from flask_cors import CORS

app = Flask(__name__, static_folder="../frontend/build")
db = setup_db(app)

bcrypt = Bcrypt(app)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

dateFormat = "%m/%d/%Y,%H:%M:%S"