from bson.objectid import ObjectId
import pymongo
from models.maindata import MainData
from auth_handler import requires_admin, requires_auth
from flask import abort, jsonify, Blueprint, request

level = Blueprint('level', __name__)

CATEGORY_NAME = "level"

@level.route('/level', methods=['POST'])
# @requires_auth
# @requires_admin
def create_subsytem():
    print("creating a level")
    data = request.json
    if (data.get('name') == '' or (not data.get("parent_id"))):
        abort(422)
    level = MainData.collection.find_one({"name": data.get('name'), "parentId": data.get("parent_id")})
    if level:
        return jsonify({
            'status': 'fail',
            'message': 'level already exist.'
        }), 404
    else:
        try:
            level = MainData(
                name=data.get('name'),
                rank=data.get('rank', 0),
                category=CATEGORY_NAME,
                subsystemId=data.get("subsystem_id"),
                parentId=[data.get("parent_id")]
            )

            # insert the level
            level.save()

            # get the data
            levels = list(MainData.collection.find({"category": CATEGORY_NAME,
             "parentId": data.get("parent_id")}))
            result= []
            for val in levels:
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


@level.route('/level/<level_id>', methods=['PUT'])
# @requires_auth
# @requires_admin
def update_subsytem(level_id):
    print("update a level")
    data = request.json
    if (data.get('name') == ''):
        abort(422)
    level = MainData.collection.find_one(dict(_id=ObjectId(level_id)))
    if not level:
        return jsonify({
            'status': 'fail',
            'message': 'level does not exist.'
        }), 404
    else:
        try:
            ## update level
            value = MainData.collection.find_one(dict(_id=ObjectId(level_id)))
            if not(data.get('rank')) or int(value.get("rank")) == int(data.get('rank')):
                MainData.collection.update_one(
                    dict(_id=ObjectId(level_id)), {
                        "$set": {"name": data.get('name'), "rank": value.get('rank')}})
            else:
                MainData(
                    **{"_id": level_id, "name": data.get(
                        'name'), "rank": data.get('rank')}).update(value)


            # get the data
            levels = list(MainData.collection.find({"category": CATEGORY_NAME,
             "subsystemId": data.get("subsystem_id")}))
            result= []
            for val in levels:
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


@level.route('/level', methods=['GET'])
def get_levels():
    print("level get")
    print(request.args.get("parentId"))
    if request.args.get("parentId"):
        levels = list(MainData.collection.find(
            {"category": CATEGORY_NAME, "parentId": request.args.get("parentId")}).sort(
                    "rank", pymongo.ASCENDING))
    else:
        levels = list(MainData.collection.find(
            {"category": CATEGORY_NAME}).sort(
                    "rank", pymongo.ASCENDING))
    result= []
    for val in levels:
        result.append(MainData(**val).to_json())
    return jsonify({'data': result, 'status': 'success'})

@level.route('/level/<level_id>', methods=['DELETE'])
# @requires_auth
# @requires_admin
def delete_levels(level_id):
    print("level Delete")
    try:
        data = MainData.collection.find_one_and_delete(
            {"_id": ObjectId(level_id)})
        MainData(**data).rankUpdate(data.get("rank"), by=-1)
    except Exception:
        import traceback
        traceback.print_exc()
        abort(500)
    return jsonify({'status': "success", "deleted": level_id})

@level.route('/level/<level_id>', methods=['GET'])
# @requires_auth
# @requires_admin
def get_one_level(level_id):
    print("get one level")
    try:
        data = MainData.collection.find_one(
            {"_id": ObjectId(level_id)})
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