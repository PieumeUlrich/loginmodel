from bson.objectid import ObjectId
import pymongo
from models.maindata import MainData
from auth_handler import requires_admin, requires_auth
from flask import abort, jsonify, Blueprint, request
from models.users import User

classes = Blueprint("classes", __name__)


@classes.route("/class", methods=["POST"])
# @requires_auth
# @requires_admin
def create_class():
    data = request.json
    if (data.get('name') == '' or data.get('parent_id')):
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
