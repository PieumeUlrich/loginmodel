from bson.objectid import ObjectId
import pymongo
from models.maindata import MainData
from auth_handler import requires_admin, requires_auth
from flask import abort, jsonify, Blueprint, request
from models.users import User

specialty = Blueprint('specialty', __name__)

CATEGORY_NAME = "specialty"

@specialty.route('/specialty', methods=['POST'])
# @requires_auth
# @requires_admin
def create_speciality():
    print("creating a specialty")
    data = request.json
    if (data.get('name') == ''):
        abort(422)
    specialty = MainData.collection.find_one({"name": data.get('name')})
    if specialty:
        return jsonify({
            'status': 'fail',
            'message': 'specialty already exist.'
        }), 404
    else:
        try:
            specialty = MainData(
                name=data.get('name'),
                category=CATEGORY_NAME,
                subsectionId=data.get("subsection_id"),
                parentId=[data.get("parent_id")],
                createdBy=User.decode_auth_token(request.headers.get('Authorization').split(" ")[1])
            )

            # insert the specialty
            specialty.save()

            # get the data
            specialtys = list(MainData.collection.find({"category": CATEGORY_NAME,
             "parentId": data.get("parent_id")}))
            result= []
            for val in specialtys:
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


@specialty.route('/specialty/<specialty_id>', methods=['PUT'])
# @requires_auth
# @requires_admin
def update_subsytem(specialty_id):
    print("update a specialty")
    data = request.json
    if (data.get('name') == ''):
        abort(422)
    specialty = MainData.collection.find_one(dict(_id=ObjectId(specialty_id)))
    if not specialty:
        return jsonify({
            'status': 'fail',
            'message': 'specialty does not exist.'
        }), 404
    else:
        try:
            ## update specialty
            value = MainData.collection.find_one(dict(_id=ObjectId(specialty_id)))
            MainData.collection.update_one(
                dict(_id=ObjectId(specialty_id)), {
                    "$set": {"name": data.get('name'), "updatedOn": datetime.now().strftime(dateFormat)}})


            # get the data
            specialtys = list(MainData.collection.find({"category": CATEGORY_NAME,
             "subsystemId": data.get("subsystem_id")}))
            result= []
            for val in specialtys:
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


@specialty.route('/specialty', methods=['GET'])
def get_specialtys():
    print("specialty get")
    print(request.args.get("parentId"))
    if request.args.get("parentId"):
        specialtys = list(MainData.collection.find(
            {"category": CATEGORY_NAME, "parentId": 
                request.args.get("parentId")}).sort(
                    "name", pymongo.ASCENDING))
    else:
        specialtys = list(MainData.collection.find(
            {"category": CATEGORY_NAME}).sort(
                    "name", pymongo.ASCENDING))
    result= []
    for val in specialtys:
        result.append(MainData(**val).to_json())
    return jsonify({'data': result, 'status': 'success'})

@specialty.route('/specialty/<specialty_id>', methods=['DELETE'])
# @requires_auth
# @requires_admin
def delete_specialtys(specialty_id):
    print("specialty Delete")
    try:
        data = MainData.collection.find_one_and_delete(
            {"_id": ObjectId(specialty_id)})
    except Exception:
        import traceback
        traceback.print_exc()
        abort(500)
    return jsonify({'status': "success", "deleted": specialty_id})


@specialty.route('/specialty/<specialty_id>', methods=['GET'])
# @requires_auth
# @requires_admin
def get_one_specialty(specialty_id):
    print("get one specialty")
    try:
        data = MainData.collection.find_one(
            {"_id": ObjectId(specialty_id)})
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