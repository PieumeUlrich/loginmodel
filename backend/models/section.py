from setup import db, dateFormat
import flask_pymongo
from datetime import datetime

class Section():
    collection = db.section
    
    def __init__(self, _id=None, name="", createdOn=datetime.now().strftime(dateFormat),
                updatedOn=datetime.now().strftime(dateFormat), createdBy=None, updatedBy=None):
        self.name = name
        self.updatedOn = updatedOn
        self.createdOn = createdOn
        self.createdBy = createdBy
        self.updatedBy = updatedBy
        self._id = _id

    def save(self):
        self.collection.insert_one({"name": self.name, "createdBy": self.createdBy, "createdOn": self.createdOn})

    def update(self, prev):
        Section.collection.update_one(dict(_id=flask_pymongo.ObjectId(self._id)), {"$set":{"name": self.name, "updatedBy": self.updatedBy, "updatedOn":self.updatedOn}})


    def to_json(self):
        return {
            "name": self.name, 
            "_id": str(self._id),
        }