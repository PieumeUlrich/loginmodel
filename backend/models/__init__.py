from flask_pymongo import PyMongo, ObjectId


# database_path = 'mongodb://flaskuser:myboy12tobe12@localhost:27017/distancelearningdb'
database_path = 'mongodb://localhost:27017/loginmodel'

def setup_db(app, database_path=database_path):
    app.config["MONGO_URI"] = database_path
    mongo = PyMongo(app)
    return mongo.db