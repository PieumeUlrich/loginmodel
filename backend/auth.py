# auth.py
from datetime import datetime
from flask import redirect, url_for, request, flash, jsonify, make_response
from flask_login import login_user, logout_user, login_required, LoginManager
from flask_restx import Resource, Namespace
from models import User
from flask_cors import cross_origin
from flask_jwt_extended import (create_access_token, create_refresh_token,
get_jwt_identity, jwt_required)

success_msg = {"msg": "Successfully Added !", 'status':201}
error_msg = {"msg": "An error occured !"}
login_msg_success = {"msg": "Login Successful !"}
logout_msg_success = {"msg": "Logout Successful !"}

auth = Namespace('auth', description='Authentication')


@auth.route('/signup')
class CreateUsers(Resource):
    # @auth.marshal_with(user_model)
    def post(self):
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


@auth.route('/login')
class Login(Resource):
    def post(self):
        data = request.get_json()

        email = data['email']
        password = data['password']
        remember = True if data['remember'] else False

        user = User.query.filter_by(email=email).first()

        # check if user actually exists
        # take the user supplied password, hash it, and compare it to the hashed password in database

        # if user.is_authenticated:
        #     return redirect("/user/users")


        if user and user.check_password(password=password):

            access_token = create_access_token(identity=user.email)
            refresh_token = create_refresh_token(identity=user.email)

            login_user(user, remember=remember)
            return make_response(jsonify(
                login_msg_success,
                {
                    "access_token":access_token,
                    "refresh_token":refresh_token,
                    "status": 201,
                    "user": {"id":user.id, "name":user.name, "email":user.email}
                }), 201)
        return make_response(jsonify(error_msg, {"status":202}), 202) # if user doesn't exist or password is wrong, reload the page
        # if the above check passes, then we know the user has the right credentials

@auth.route('/logout')
class LogoutUser(Resource):
    # @jwt_required
    def get(self):
        logout_user()
        return make_response(jsonify(logout_msg_success), 201)


@auth.route('/refresh')
class RefreshResource(Resource):
    @jwt_required(refresh=True)
    def post(self):
        cur_user = get_jwt_identity()
        new_access_token = create_access_token(identity=cur_user)
        return make_response(jsonify({"access_token":new_access_token}), 200)


# @login_manager.user_loader
# def load_user(user_id):
#     """Check if user is logged-in on every page load."""
#     if user_id is not None:
#         return User.query.get(user_id)
#     return None


# @login_manager.unauthorized_handler
# def unauthorized():
#     """Redirect unauthorized users to Login page."""
#     flash('You must be logged in to view that page.')
#     return redirect(url_for('auth_bp.login'))