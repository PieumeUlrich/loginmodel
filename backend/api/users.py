from bson.objectid import ObjectId
import pymongo
from models.users import User
from auth_handler import requires_admin, requires_auth
from flask import abort, jsonify, Blueprint, request

user = Blueprint('user', __name__)

@user.route('/users', methods=['GET'])
@requires_auth
@requires_admin
def get_users():
    print("User status")
    users = User.collection.find().sort("registeredOn", pymongo.ASCENDING)
    result = []
    for user in users:
        user = User(**user).to_json()
        result.append(user)
    return jsonify({'data': result, 'status': 'success'})

@user.route('/users/<user_id>', methods=['DELETE'])
@requires_auth
@requires_admin
def delete_users(user_id):
    print("User Delete")
    try:
        User.collection.delete_one({"_id": ObjectId(user_id)})
    except Exception:
        abort(500)
    return jsonify({'status': "success", "deleted": user_id})

@user.route('/users/<user_id>', methods=['PUT'])
@requires_auth
@requires_admin
def update_users(user_id):
    print("Updating User")
    # try:
    User.collection.update_one({"_id": ObjectId(user_id)}, {'$set': {
    'email': request.json['email'],
    'name': request.json['name'],
    'admin': True if request.json['admin'] else False
    }})
    # except Exception:
    #     abort(500)
    return jsonify({'status': "success", "updated": user_id})