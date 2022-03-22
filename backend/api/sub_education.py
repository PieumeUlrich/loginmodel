from bson.objectid import ObjectId
import pymongo
from models.maindata import MainData
from auth_handler import requires_admin, requires_auth
from flask import abort, jsonify, Blueprint, request
from models.users import User
from setup import dateFormat
from datetime import datetime

sub_education = Blueprint('sub_education', __name__)

CATEGORY_NAME = "sub_education"

@sub_education.route('/sub_education', methods=['POST'])
# @requires_auth
# @requires_admin
def create_subsytem():
    print("creating a sub_education")
    data = request.json
    if (data.get('name') == '') or (not data.get("parent_id")):
        abort(422)
    sub_education = MainData.collection.find_one({"name": data.get('name'), "parentId": data.get("parent_id")})
    if sub_education:
        return jsonify({
            'status': 'fail',
            'message': 'sub_education already exist.'
        }), 404
    else:
        try:
            sub_education = MainData(
                name=data.get('name'),
                category=CATEGORY_NAME,
                subsectionId=data.get("subsection_id"),
                parentId=[data.get("parent_id")],
                createdBy=User.decode_auth_token(request.headers.get('Authorization').split(" ")[1])
            )

            # insert the sub_education
            sub_education.save()

            # get the data
            sub_educations = list(MainData.collection.find({"category": CATEGORY_NAME,
             "parentId": data.get("parent_id")}))
            result= []
            for val in sub_educations:
                result.append(MainData(**val).to_json())
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


@sub_education.route('/sub_education/<sub_education_id>', methods=['PUT'])
# @requires_auth
# @requires_admin
def update_subsytem(sub_education_id):
    print("update a sub_education")
    data = request.json
    if (data.get('name') == ''):
        abort(422)
    sub_education = MainData.collection.find_one(dict(_id=ObjectId(sub_education_id)))
    if not sub_education:
        return jsonify({
            'status': 'fail',
            'message': 'sub_education does not exist.'
        }), 404
    else:
        try:
            ## update sub_education
            value = MainData.collection.find_one(dict(_id=ObjectId(sub_education_id)))
            MainData.collection.update_one(
                dict(_id=ObjectId(sub_education_id)), {
                    "$set": {"name": data.get('name'), "updatedOn":datetime.now().strftime(dateFormat),
                    "updatedBy":User.decode_auth_token(request.headers.get('Authorization').split(" ")[1])}})


            # get the data
            sub_educations = list(MainData.collection.find({"category": CATEGORY_NAME,
             "subsystemId": data.get("subsystem_id")}))
            result= []
            for val in sub_educations:
                result.append(MainData(**val).to_json())
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


@sub_education.route('/sub_education', methods=['GET'])
def get_sub_educations():
    print("sub_education get")
    print(request.args.get("education_id"))
    if request.args.get("education_id"):
        sub_educations = list(MainData.collection.find(
            {"category": CATEGORY_NAME, "parentId": request.args.get("education_id") }).sort(
                    "name", pymongo.ASCENDING))
    else:
        sub_educations = list(MainData.collection.find(
            {"category": CATEGORY_NAME}).sort(
                    "name", pymongo.ASCENDING))
    result= []
    for val in sub_educations:
        result.append(MainData(**val).to_json())
    return jsonify({'data': result, 'status': 'success'})

@sub_education.route('/sub_education/<sub_education_id>', methods=['DELETE'])
# @requires_auth
# @requires_admin
def delete_sub_educations(sub_education_id):
    print("sub_education Delete")
    try:
        data = MainData.collection.find_one_and_delete(
            {"_id": ObjectId(sub_education_id)})
    except Exception:
        import traceback
        traceback.print_exc()
        abort(500)
    return jsonify({'status': "success", "deleted": sub_education_id})

@sub_education.route('/sub_education/<sub_education_id>', methods=['GET'])
# @requires_auth
# @requires_admin
def get_one_sub_educations(sub_education_id):
    print("Get one sub education with its _id")
    try:
        data = MainData.collection.find_one(
            {"_id": ObjectId(sub_education_id)})
        data = MainData(**data).to_json()
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