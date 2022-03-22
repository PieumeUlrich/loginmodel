from bson.objectid import ObjectId
from setup import dateFormat
from datetime import datetime
import pymongo
from models.section import Section
from auth_handler import requires_admin, requires_auth
from flask import abort, jsonify, Blueprint, request

section = Blueprint('section', __name__)


@section.route('/section', methods=['POST'])
@requires_auth
# @requires_admin
def create_section():
    from models.users import User
    user = User.decode_auth_token(request.headers.get('Authorization').split(" ")[1])
    data = request.json
    if (data.get('name') == ''):
        abort(422)
    section = Section.collection.find_one(dict(name=data.get('name')))
    if section:
        return jsonify({
            'status': 'fail',
            'message': 'section already exist.'
        }), 404
    else:
        try:
            section = Section(
                name=data.get('name'),
                createdBy= user,
                createdOn= datetime.now().strftime(dateFormat)
            )

            # insert the section
            section.save()

            # get the data
            sections = Section.collection.find()
            result= []
            for val in sections:
                result.append(Section(**val).to_json())
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


@section.route('/section/<section_id>', methods=['PUT'])
@requires_auth
# @requires_admin
def update_section(section_id):
    from models.users import User
    user = User.decode_auth_token(request.headers.get('Authorization').split(" ")[1])

    print("update a section")
    data = request.json
    if (data.get('name') == ''):
        abort(422)
    section = Section.collection.find_one(dict(_id=ObjectId(section_id)))
    if not section:
        return jsonify({
            'status': 'fail',
            'message': 'section does not exist.'
        }), 404
    else:
        try:
            ## update section
            value = Section.collection.find_one(dict(_id=ObjectId(section_id)))
            Section.collection.update_one(dict(_id=ObjectId(section_id)), {"$set": {"name": data.get('name'), "updatedBy": user, "updatedOn": datetime.now().strftime(dateFormat)}})


            # get the data
            sections = Section.collection.find()
            result= []
            for val in sections:
                result.append(Section(**val).to_json())
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


@section.route('/section', methods=['GET'])
def get_sections():
    print("section get")
    # update_french_section_info()
    sections = list(Section.collection.find().sort("name", pymongo.ASCENDING))
    result= []
    for val in sections:
        result.append(Section(**val).to_json())
    return jsonify({'data': result, 'status': 'success'})

@section.route('/section/<section_id>', methods=['DELETE'])
@requires_auth
# @requires_admin
def delete_sections(section_id):
    print("section Delete")
    try:
        data = Section.collection.find_one_and_delete({"_id": ObjectId(section_id)})
    except Exception:
        import traceback
        traceback.print_exc()
        abort(500)
    return jsonify({'status': "success", "deleted": section_id})

@section.route('/section/<section_id>', methods=['GET'])
@requires_auth
# @requires_admin
def get_one_section(section_id):
    print("get one section")
    try:
        data = Section.collection.find_one(
            {"_id": ObjectId(section_id)})
        data = Section(**data).to_json()
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


# def update_french_section_info():
#     from models.maindata import MainData
#     enseignment_general = MainData.collection.find_one(dict(name="ENSEIGNEMENT GÉNÉRAL"))
#     enseignment_general = MainData(**enseignment_general).to_json()
#     print(enseignment_general)
#     print("YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY")
#     fr_sub_education_1 = MainData.collection.find_one({"name": "1ere Cycle"})
#     if fr_sub_education_1:
#         return
#     fr_sub_education_1 = MainData(
#                 name="1ere Cycle",
#                 rank=0,
#                 category="sub_education",
#                 sectionId=enseignment_general["sectionId"],
#                 parentId=[enseignment_general['_id']]
#             )
#     fr_sub_education_2 = MainData(
#                 name="2nd Cycle",
#                 rank=0,
#                 category="sub_education",
#                 sectionId=enseignment_general["sectionId"],
#                 parentId=[enseignment_general['_id']]
#             )
#     # insert the sub_education
#     fr_sub_education_1.save()
#     fr_sub_education_1 = MainData.collection.find_one({"name": fr_sub_education_1.name, "parentId": enseignment_general['_id']})
#     fr_sub_education_1 = MainData(**fr_sub_education_1).to_json()
#     fr_sub_education_2.save()
#     fr_sub_education_2 = MainData.collection.find_one({"name": fr_sub_education_2.name, "parentId": enseignment_general['_id']})
#     fr_sub_education_2 = MainData(**fr_sub_education_2).to_json()

#     classess = list(MainData.collection.find(
#             {"category": "classes", "parentId": enseignment_general['_id'] }).sort(
#                     "rank", pymongo.ASCENDING))

#     some_class = classess[:4]
#     form4and5 = classess[4:]
#     general(some_class, fr_sub_education_1, enseignment_general)
#     with_science_arts(form4and5, fr_sub_education_2, enseignment_general)


# def update_section_info():
#     from models.maindata import MainData
#     general_education = MainData.collection.find_one(dict(name="GENERAL EDUCATION"))
#     general_education = MainData(**general_education).to_json()
#     enseignment_general = MainData.collection.find_one(dict(name="ENSEIGNEMENT GÉNÉRAL"))
#     enseignment_general = MainData(**enseignment_general).to_json()

#     sub_education_1 = MainData.collection.find_one({"name": "1st Cycle"})
#     if sub_education_1:
#         return
#     sub_education_1 = MainData(
#                 name="1st Cycle",
#                 rank=0,
#                 category="sub_education",
#                 sectionId=general_education["sectionId"],
#                 parentId=[general_education['_id']]
#             )
#     sub_education_2 = MainData(
#                 name="2nd Cycle",
#                 rank=0,
#                 category="sub_education",
#                 sectionId=general_education["sectionId"],
#                 parentId=[general_education['_id']]
#             )
#     # insert the sub_education
#     sub_education_1.save()
#     sub_education_1 = MainData.collection.find_one({"name": sub_education_1.name, "parentId": general_education['_id']})
#     sub_education_1 = MainData(**sub_education_1).to_json()
#     sub_education_2.save()
#     sub_education_2 = MainData.collection.find_one({"name": sub_education_2.name, "parentId": general_education['_id']})
#     sub_education_2 = MainData(**sub_education_2).to_json()


#     classess = list(MainData.collection.find(
#             {"category": "classes", "parentId": general_education['_id'] }).sort(
#                     "rank", pymongo.ASCENDING))

#     some_class = classess[:3]
#     form4and5 = classess[3:5]
#     lowerAndUpper = classess[5:]
#     general(some_class, sub_education_1, general_education)
#     with_science_arts(form4and5, sub_education_1, general_education)
#     with_science_arts(lowerAndUpper, sub_education_2, general_education)


# def with_science_arts(classess, sub_education, general_education):
#     from models.maindata import MainData
#     v_class = MainData(**classess[-1]).to_json()
    
#     levelses = list(MainData.collection.find(
#                 {"category": "level", "parentId": v_class['_id'] }).sort(
#                         "rank", pymongo.ASCENDING))
#     print(levelses)
#     print('OOOOOOOOOOOOOOOOOOOOOOOOOOOO')
#     print(classess[-1])
#     levels_dict = {}
#     for s_level in levelses:
#         s_level = MainData(**s_level).to_json()
#         print(s_level['name'])
#         new_level = MainData.collection.find_one({"name": s_level['name'].lower(), "parentId": sub_education.get('_id')})
#         if(not new_level):
#             print('2 I am jerererererererere')
#             new_level = MainData(
#             name=s_level['name'].lower(),
#             rank=0,
#             category="classes",
#             sectionId=general_education['sectionId'],
#             parentId= [sub_education.get('_id')]
#             )
#             new_level.save()
#         new_level = MainData.collection.find_one({"name": s_level['name'].lower(), "parentId": sub_education.get('_id')})
#         new_level = MainData(**new_level).to_json()
#         levels_dict[s_level['name'].lower()] = new_level
#         from pprint import pprint
#         pprint(levels_dict)
#     for classe in classess:
#         classe = MainData(**classe).to_json()
#         levels = list(MainData.collection.find(
#             {"category": "level", "parentId": classe['_id'] }).sort(
#                     "rank", pymongo.ASCENDING))
#         for level in levels:
#             level = MainData(**level).to_json()
#             level_names = levels_dict.keys()
#             for level_name in level_names:
#                 if level["name"].lower() == level_name.lower():
#                     new_class = MainData.collection.find_one({"name": classe['name'].lower(), "parentId": str(levels_dict[level_name]['_id']) })
#                     if(not new_class):
#                         new_class = MainData(
#                                     name=classe['name'].lower(),
#                                     rank=0,
#                                     category="level",
#                                     sectionId=general_education['sectionId'],
#                                     parentId= [str(levels_dict[level_name]['_id'])]
#                                 )
#                         new_class.save()
#                         new_class = MainData.collection.find_one({"name": classe['name'].lower(), "parentId": str(levels_dict[level_name]['_id']) })
#                     new_class = MainData(**new_class).to_json()
#                     subjects = list(MainData.collection.find(
#                     {"category": "subject", "parentId": level['_id'] }).sort(
#                             "rank", pymongo.ASCENDING))
#                     other_subjects = list(MainData.collection.find(
#                     {"category": "subject", "parentId": classe['_id'] }).sort(
#                             "rank", pymongo.ASCENDING))
#                     subjects = subjects + other_subjects
#                     for subject in subjects:
#                         subject = MainData(**subject).to_json()
#                         MainData.collection.update_one(
#                             dict(_id=ObjectId(subject['_id'])), {
#                                 "$set": {"parentId": [new_class['_id']]}})
#         MainData.collection.find_one_and_delete({"_id": ObjectId(classe['_id'])})


# def general(classess, sub_education_1, general_education):
#     from models.maindata import MainData
#     for classe in classess:
#         classe = MainData(**classe).to_json()
#         levels = list(MainData.collection.find(
#             {"category": "level", "parentId": classe['_id'] }).sort(
#                     "rank", pymongo.ASCENDING))
#         # if len(levels) == 0:
#         print('I am jerererererererere')
#         new_level = MainData.collection.find_one({"name": 'General', "parentId": sub_education_1.get('_id')})
#         if(not new_level):
#             print('2 I am jerererererererere')
#             new_level = MainData(
#             name='General',
#             rank=0,
#             category="classes",
#             sectionId=general_education['sectionId'],
#             parentId= [sub_education_1.get('_id')]
#             )
#             new_level.save()
#         new_level = MainData.collection.find_one({"name": 'General', "parentId": sub_education_1.get('_id')})
#         new_level = MainData(**new_level).to_json()
#         MainData.collection.update_one(
#                 dict(_id=ObjectId(classe['_id'])), {
#                     "$set": {"parentId": [new_level['_id']], 'category': "level"}})
            


