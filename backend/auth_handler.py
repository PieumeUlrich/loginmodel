from functools import wraps
from flask import request, g, jsonify
from flask_pymongo import ObjectId
from models.users import User


def requires_auth(f):
    """
    Decorator function which verifies if browser token belong to that user in our databse
    i.e if that user has been authenticated
    :param f: function
    :return:
    """
    @wraps(f)
    def decorated(*args, **kwargs):

        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            print(auth_token)
            resp = User.decode_auth_token(auth_token)
            if resp != None or "Please" not in resp:
                print(resp)
                user = User.collection.find_one({"_id": ObjectId(resp)})
                if user:
                    user = User(**user).to_json()
                else:
                    return jsonify(dict(message="User does not exist", status='fail')), 401
                # print(user)
                if user:
                    g.current_user = user
                    return f(*args, **kwargs)
            return jsonify(dict(message=resp, status='fail')), 401

        return jsonify(dict(message="Authentication is required to access this resource", status='fail')), 401

    return decorated


def requires_admin(f):
    """
    Decorated function which checks if the current user is the admin
    :param f: function
    :return:
    """
    @wraps(f)
    def decorated(*args, **kwargs):

        # Get the currently logged in user.
        user_id = g.current_user['_id']
        user = User.collection.find_one({"_id": ObjectId(user_id)})
        # Checking if the logged in user is the admin. If yes grant access.
        permission = user['admin']
        if not permission:
            resp = dict(message="You Don't have permission to access this resource!", status="fail")
            return jsonify(resp), 401
        return f(*args, **kwargs)
    return decorated