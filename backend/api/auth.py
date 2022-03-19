from models.blacklistedToken import BlacklistToken
from flask import request, abort, jsonify, Blueprint
from setup import bcrypt
from flask_pymongo import ObjectId

from models.users import BCRYPT_LOG_ROUNDS, User

auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['POST'])
def signup_user():
    print("Registering a user")
    data = request.json
    if ((data.get('email') == '') or (data.get('password') == '')):
        abort(422)
    user = User.collection.find_one(dict(email=data.get('email')))
    if not user:
        try:
            user = User(
                name=data.get('name'),
                email=data.get('email'),
                password=bcrypt.generate_password_hash(
                    data.get('password'), BCRYPT_LOG_ROUNDS).decode(),
                admin=True if data.get('admin') else False
            )

            # insert the user
            user.save()

            # generate the auth token
            user = User.collection.find_one(dict(email=data.get('email')))
            auth_token = User.encode_auth_token(str(user.get("_id")))
            responseObject = {
                'status': 'success',
                'message': 'Successfully registered.',
                'auth_token': auth_token
            }
            return jsonify(responseObject), 201
        except Exception as e:
            import traceback
            traceback.print_exc()
            abort(401)
    else:
        responseObject = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return jsonify(responseObject), 202


@auth.route('/login', methods=['POST'])
def login_user():
    data = request.json
    if ((data.get('email') == '') or (data.get('password') == '')):
        abort(422)
    user = User.collection.find_one(dict(email=data.get('email')))
    if not user:
        return jsonify({
            'status': 'fail',
            'message': 'User does not exist.'
        }), 404

    if not bcrypt.check_password_hash(
        user.get("password"), data.get('password')
    ):
        # abort(401)
        return jsonify({
            'status': 'fail',
            'message': 'Password incorrect!',
        }), 401

    try:
        # fetch the user data
        auth_token = User.encode_auth_token(str(user.get("_id")))
        if auth_token:
            responseObject = {
                'status': 'success',
                'message': 'Successfully logged in.',
                'auth_token': auth_token
            }
            return jsonify(responseObject), 200
    except Exception as e:
        print(e)
        responseObject = {
            'status': 'fail',
            'message': 'Try again'
        }
        return jsonify(responseObject), 500

@auth.route('/status', methods=['GET'])
def user_token_status():
    print("User status")
    auth_header = request.headers.get('Authorization')
    if auth_header:
        try:
            auth_token = auth_header.split(" ")[1]
        except IndexError:
            responseObject = {
                'status': 'fail',
                'message': 'Bearer token malformed.'
            }
            return jsonify(responseObject), 401
    else:
        auth_token = ''
    if auth_token:
        resp = User.decode_auth_token(auth_token)
        if "Please" not in resp:
            user = User.collection.find_one({"_id": ObjectId(resp)})
            user = User(**user).to_json()
            responseObject = {
                'status': 'success',
                'data': user
            }
            return jsonify(responseObject), 200
        responseObject = {
            'status': 'fail',
            'message': resp
        }
        return jsonify(responseObject), 401
    else:
        responseObject = {
            'status': 'fail',
            'message': 'Provide a valid auth token.'
        }
        return jsonify(responseObject), 401

@auth.route('/logout', methods=['POST'])
def logout_user():
    print("User status")
    auth_header = request.headers.get('Authorization')
    auth_token = auth_header.split(" ")[1]
    # mark the token as blacklisted
    blacklist_token = BlacklistToken(token=auth_token)
    try:
        # insert the token
        blacklist_token.save()
        responseObject = {
            'status': 'success',
            'message': 'Successfully logged out.'
        }
        return jsonify(responseObject), 200
    except Exception as e:
        responseObject = {
            'status': 'fail',
            'message': e
        }
        return jsonify(responseObject), 200