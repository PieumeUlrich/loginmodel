from datetime import datetime

from flask import Flask, Blueprint, jsonify, make_response, request
from models import User
from exts import db
from flask_cors import CORS
from config import ProdConfig
from config import DevConfig

from flask_jwt_extended import (create_access_token, create_refresh_token,
get_jwt_identity, jwt_required)
from flask_login import login_user, logout_user, login_required, LoginManager
from flask_jwt_extended import JWTManager


#Response messages going to the frontend
success_msg = {"msg": "Successfully Added !", 'status':201}
error_msg = {"msg": "An error occured !"}
login_msg_success = {"msg": "Login Successful !"}
logout_msg_success = {"msg": "Logout Successful !"}



app = Flask(__name__)
CORS(app)
db.init_app(app)
JWTManager(app)
login_manager = LoginManager()
login_manager.init_app(app)



@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def Index():
	user = {'username': 'Miguel'}
	posts = [
		{
			'author': {'username': 'John'},
			'body': 'Beautiful day in Portland!'
		},
		{
			'author': {'username': 'Susan'},
			'body': 'The Avengers movie was so cool!'
		}
	]
	return jsonify({"posts":posts, "users":user})


@app.route('/users', methods=['GET'])
@jwt_required()
def Users():
	users = list()
	for user in User.query.all():
		users.append({'name':user.name, 'email': user.email})
	return jsonify(users)



@app.route('/signup', methods=['POST'])
def signup():
	data = request.get_json()
	email = data['email']
	name = data['name']
	password = data['password']
	user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

	if user: # if a user is found, we want to redirect back to signup page so user can try again  
		return make_response(jsonify({'msg':'Email address already exist !', 'status': 202}), 202)

    # create new user with the form data. Hash the password so plaintext version isn't saved.

	new_user = User(email=email, name=name, created_on=datetime.utcnow(), update_on=datetime.utcnow())
	new_user.set_password(password)

    # add the new user to the database
	new_user.save()

	return make_response(jsonify(success_msg), 201)


@app.route('/login', methods=['POST'])
def login():
	data = request.get_json()

	email = data['email']
	password = data['password']
	remember = True if data['remember'] else False

	user = User.query.filter_by(email=email).first()

	# check if user actually exists
	# take the user supplied password, hash it, and compare it to the hashed password in database

	if user and user.check_password(password=password):

		access_token = create_access_token(identity=user.email)
		refresh_token = create_refresh_token(identity=user.email)

		login_user(user, remember=remember)
		return make_response(jsonify(
			login_msg_success, {
			"access_token":access_token,
			"refresh_token":refresh_token,
			"status": 201,
			"user": {"id":user.id, "name":user.name, "email":user.email}
		}), 201)
	return make_response(jsonify(error_msg, {"status":202}), 202) # if user doesn't exist or password is wrong, reload the page
    # if the above check passes, then we know the user has the right credentials


@app.route('/refresh', methods=['POST'])
# @jwt_required(refresh=True)
def RefreshResource(Resource):
	cur_user = get_jwt_identity()
	new_access_token = create_access_token(identity=cur_user)
	return make_response(jsonify({"access_token":new_access_token}), 200)


if __name__ == "__main__":
	app.config.from_object(DevConfig)
	# app.run(debug=True, host='0.0.0.0', port=8080)
	app.run(debug=True)