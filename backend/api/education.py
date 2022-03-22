from bson.objectid import ObjectId
import pymongo
from models.maindata import MainData
from auth_handler import requires_admin, requires_auth
from flask import abort, jsonify, Blueprint, request
from models.users import User

education = Blueprint('education', __name__)

CATEGORY_NAME = "education"

@education.route('/education', methods=['POST'])
# @requires_auth
# @requires_admin
def create_subsytem():
    print("creating a education")
    data = request.json
    if (data.get('name') == '') or (not data.get("parent_id")):
        abort(422)
    education = MainData.collection.find_one({"name": data.get('name'), "parentId": data.get("parent_id")})
    if education:
        return jsonify({
            'status': 'fail',
            'message': 'education already exist.'
        }), 404
    else:
        try:
            education = MainData(
                name=data.get('name'),
                category=CATEGORY_NAME,
                subsectionId=data.get("subsection_id"),
                parentId=[data.get("parent_id")],
                createdBy=User.decode_auth_token(request.headers.get('Authorization').split(" ")[1])
            )

            # insert the education
            education.save()

            # get the data
            educations = list(MainData.collection.find({"category": CATEGORY_NAME,
             "subsystemId": data.get("subsystem_id")}))
            result= []
            for val in educations:
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


@education.route('/education/<education_id>', methods=['PUT'])
# @requires_auth
# @requires_admin
def update_subsytem(education_id):
    print("update a education")
    data = request.json
    if (data.get('name') == ''):
        abort(422)
    education = MainData.collection.find_one(dict(_id=ObjectId(education_id)))
    if not education:
        return jsonify({
            'status': 'fail',
            'message': 'education does not exist.'
        }), 404
    else:
        try:
            ## update education
            value = MainData.collection.find_one(dict(_id=ObjectId(education_id)))
            MainData.collection.update_one(
                dict(_id=ObjectId(education_id)), {
                    "$set": {"name": data.get('name'), "updatedBy":User.decode_auth_token(request.headers.get('Authorization').split(" ")[1])}})

            # get the data
            educations = list(MainData.collection.find({"category": CATEGORY_NAME,
             "subsectionId": data.get("subsection_id")}))
            result= []
            for val in educations:
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


@education.route('/education', methods=['GET'])
def get_educations():
    print(request.args.get("subsystem_id"))
    if request.args.get("subsystem_id"):
        educations = list(MainData.collection.find(
            {"category": CATEGORY_NAME, "subsectionId": 
                str(request.args.get("subsystem_id"))}).sort(
                    "name", pymongo.ASCENDING))
    else:
        educations = list(MainData.collection.find(
            {"category": CATEGORY_NAME}).sort(
                    "name", pymongo.ASCENDING))
    result= []
    for val in educations:
        result.append(MainData(**val).to_json())
    return jsonify({'data': result, 'status': 'success'})

@education.route('/education/<education_id>', methods=['DELETE'])
# @requires_auth
# @requires_admin
def delete_educations(education_id):
    print("education Delete")
    try:
        data = MainData.collection.find_one_and_delete(
            {"_id": ObjectId(education_id)})
    except Exception:
        import traceback
        traceback.print_exc()
        abort(500)
    return jsonify({'status': "success", "deleted": education_id})

@education.route('/education/<education_id>', methods=['GET'])
# @requires_auth
# @requires_admin
def get_one_education(education_id):
    print("get one education")
    try:
        data = MainData.collection.find_one(
            {"_id": ObjectId(education_id)})
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