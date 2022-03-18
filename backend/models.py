"""Database models."""
from flask_pymongo import PyMongo
from mongoengine import Document, connect, StringField
from pymongo import MongoClient
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = PyMongo()
client = MongoClient('localhost', 27017)
connect('loginmodel')
dbMongo = client.loginmodel
# class Users(UserMixin, db.Model):
#     """User account model."""

#     __tablename__ = 'Users'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False, unique=False)
#     email = db.Column(db.String(40), unique=True, nullable=False)
#     password = db.Column(db.String(200), primary_key=False, unique=False, nullable=False)
#     created_on = db.Column(db.DateTime, index=False, unique=False, nullable=True)
#     update_on = db.Column(db.DateTime, index=False, unique=False, nullable=True)
#     last_login = db.Column(db.DateTime, index=False, unique=False, nullable=True)

#     def set_password(self, password):
#         """Create hashed password."""
#         self.password = generate_password_hash(password, method='sha256')

#     def check_password(self, password):
#         """Check hashed password."""
#         return check_password_hash(self.password, password)


#     def save(self):
#         db.session.add(self)
#         db.session.commit()

    
#     def delete(self):
#         db.session.delete(self)
#         db.session.commit()
    

#     def update(self, name, email, update_on):
#         self.name = name
#         self.email = email
#         self.update_on = update_on

#         db.session.commit()

#     # def is_authenticated(self):
#     #     return self.is_authenticated

#     def __repr__(self):
#         return '<User {}>'.format(self.name)



class Users(UserMixin, Document):
    name = StringField()
    email = StringField()
    password = StringField()
    created_on = StringField()
    update_on = StringField()
    last_login = StringField()

    def to_json(self):
        return {
        "name": self.name,
        "email": self.email
        }

    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_anonymous():
        return False

    def get_id(self):
        return self.email

    @staticmethod
    def check_password(password_hash, password):
        return check_password_hash(password_hash, password)


#     def set_password(self, password):
#         """Create hashed password."""
#         self.password = generate_password_hash(password, method='sha256')

#     def check_password(self, password):
#         """Check hashed password."""
#         return check_password_hash(self.password, password)
