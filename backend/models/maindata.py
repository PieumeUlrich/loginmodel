import flask_pymongo
from setup import db, dateFormat
from datetime import datetime
from flask_pymongo import ObjectId

class MainData():
    collection = db.maindata

    def __init__(self, _id=None, name="", parentId=list(), subsectionId="", category="",
        createdOn=datetime.now().strftime(dateFormat), createdBy="",
        updatedOn=datetime.now().strftime(dateFormat), updatedBy=""):
        self._id = _id
        self.name = name
        self.parentId = parentId
        self.subsectionId = subsectionId
        self.category = category
        self.updatedOn = updatedOn
        self.createdOn = createdOn
        self.createdBy = createdBy
        self.updatedBy = updatedBy

    def save(self):
        maindata = self.to_json()
        maindata.pop("_id")
        self.collection.insert_one(maindata)

    def update(self, prev):
        maindata = self.to_json()
        maindata.pop("_id")
        MainData.collection.update_one(dict(_id=flask_pymongo.ObjectId(self._id)), {"$set": {"name": maindata.get("name")}})


    def to_json(self):
        parent_id_list = []
        for val in self.parentId:
            parent_id_list.append(str(val))
        return {
            "_id": str(self._id),
            "name": self.name,
            "parentId": parent_id_list,
            "subsectionId": self.subsectionId,
            "category": self.category,
            "createdOn": self.createdOn,
            "createdBy": self.createdBy
        }
    