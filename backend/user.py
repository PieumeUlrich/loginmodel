# user.py
from datetime import datetime
from flask import Blueprint, redirect, url_for, request, flash, jsonify, make_response
from flask_login import login_user, logout_user, login_required, LoginManager
from models import dbMongo as db
from flask_jwt_extended import jwt_required



from bson.json_util import dumps
from bson.objectid import ObjectId


success_msg = {"msg": "Successfully Added !"}
failure_msg = {"msg": "An error occured when adding !"}
error_msg = {"msg": "An error occured !"}
update_msg = {"msg": "Updated Successfully !"}
delete_msg = {"msg": "Deleted Successfully !"}

user = Blueprint('Users',__name__, url_prefix='/user')


# user_model = user.model(
#     "User",
#     {
#          "id": fields.Integer(),
#          "name": fields.String(),
#          "email": fields.String(),
#          "created_on": fields.DateTime(),
#          "updated_on": fields.DateTime(),
#          "last_login": fields.String()
#     }
# )

@user.route('/', methods=['GET'])
@user.route('/index', methods=['GET'])
def Index():
    users = db.users.find()
    return dumps(users)


@user.route('/users', methods=['GET'])
@jwt_required()
def Users():
    users = db.users.find()
    return dumps(users)

 
# @user.route('/user/<int:id>')
# class UserId(Resource):
#     @user.marshal_with(user_model)
#     @jwt_required()
#     def get(self, id):
#         user = User.query.get_or_404(id)
#         return user

#     # @api.marshal_with(user_model) This line tells the funcion to return data only in that format
#     @jwt_required()
#     def put(self, id):
#         cur_user = User.query.get_or_404(id)
#         udata = request.get_json()

#         cur_user.update(name=udata['name'], email=udata['email'], update_on=datetime.now())
#         return make_response(jsonify(update_msg), 201)

#     @jwt_required()
#     def delete(self, id):
#         cur_user = User.query.get_or_404(id)
#         cur_user.delete()
#         return make_response(jsonify(delete_msg), 201)

