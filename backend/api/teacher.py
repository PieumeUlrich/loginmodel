from bson.objectid import ObjectId
from bson.json_util import dumps
import pymongo
from models.teacher import Teacher
from auth_handler import requires_admin, requires_auth
from flask import abort, jsonify, Blueprint, request
from models.users import User
from setup import dateFormat
from datetime import datetime

teacher = Blueprint('teacher', __name__)


@teacher.route('/teacher', methods=['POST'])
# @requires_auth
# @requires_admin
def create_teacher():
    print("creating a teacher")
    data = request.json
    if (data.get('name') == ''):
        abort(422)
    teacher = Teacher.collection.find_one({"name": data.get('name'), "email":data.get('email')})
    if teacher:
        return jsonify({
            'status': 'fail',
            'message': 'teacher already exist.'
        }), 404
    else:
        try:
            teacher = Teacher(
                name=data.get('name'),
                email=data.get('email'),
                subject=list(),
                password=data.get("password"),
                profile_picture=data.get('profile_picture'),
                contact=data.get('contact'),
                # createdBy=User.decode_auth_token(request.headers.get('Authorization').split(" ")[1])
            )

            # insert the teacher
            teacher.save()

            # get the data
            teachers = Teacher.collection.find()
            result= []
            for val in teachers:
                result.append(Teacher(**val).to_json())
            responseObject = {
                'status': 'success',
                'message': 'Successfully added.',
                'data': result
            }
            return jsonify(responseObject), 201
        except Exception as e:
            import traceback
            traceback.print_exc()
            abort(401)


@teacher.route('/teacher/<teacher_id>', methods=['PUT'])
# @requires_auth
# @requires_admin
def update_teacher(teacher_id):
    print("update a teacher")
    data = request.json
    if (data.get('name') == '' or data.get('email') == ''):
        abort(422)
    teacher = Teacher.collection.find_one(dict(_id=ObjectId(teacher_id)))
    if not teacher:
        return jsonify({
            'status': 'fail',
            'message': 'teacher does not exist.'
        }), 404
    else:
        try:
            ## update teacher
            value = Teacher.collection.find_one(dict(_id=ObjectId(teacher_id)))
            Teacher.collection.update_one(
                dict(_id=ObjectId(teacher_id)), {
                    "$set": {"name": data.get('name'), 
                    "email": data.get('email'), "profile_picture": data.get('profile_picture'),
                    "subject": [data.get('subject')],
                    "updatedBy":User.decode_auth_token(request.headers.get('Authorization').split(" ")[1]),
                    "updatedOn": datetime.now().strftime(dateFormat)}
                })


            # get the data
            teachers = Teacher.collection.find()
            result= []
            for val in teachers:
                result.append(Teacher(**val).to_json())
            responseObject = {
                'status': 'success',
                'message': 'Successfully updated.',
                'data': result
            }
            return jsonify(responseObject), 201
        except Exception as e:
            import traceback
            traceback.print_exc()
            abort(401)


@teacher.route('/teacher', methods=['GET'])
def get_teachers():
    print("teacher get")
    print(request.args.get("parentId"))
    teachers = Teacher.collection.find()
    result= []
    result = dumps(teachers)
    # teachers = Teacher.collection.find()
    # result= []
    # for val in teachers:
    #     result.append(Teacher(**val).to_json())
    # responseObject = {
    #     'status': 'success',
    #     'message': 'Successfully added.',
    #     'data': result
    # }
    # return jsonify(responseObject), 201
    return jsonify({'data': result, 'status': 'success'})


@teacher.route('/teacher/<teacher_id>', methods=['DELETE'])
# @requires_auth
# @requires_admin
def delete_teacher(teacher_id):
    print("teacher Delete")
    try:
        data = Teacher.collection.find_one_and_delete(
            {"_id": ObjectId(teacher_id)})
    except Exception:
        import traceback
        traceback.print_exc()
        abort(500)
    return jsonify({'status': "success", "deleted": teacher_id})


@teacher.route('/teacher/<teacher_id>', methods=['GET'])
# @requires_auth
# @requires_admin
def get_one_teacher(teacher_id):
    print("get one teacher")
    try:
        data = Teacher.collection.find_one(
            {"_id": ObjectId(teacher_id)})
        data = Teacher(**data).to_json()
        responseObject = {
            'status': 'success',
            'message': 'Successfully gotten',
            'data': data
        }
    except Exception:
        import traceback
        traceback.print_exc()
        abort(500)
    return jsonify(responseObject), 201