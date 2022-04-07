from setup import db, dateFormat
from datetime import datetime, timedelta
import jwt
from .blacklistedToken import BlacklistToken

"""Production configuration."""
SECRET_KEY = 'minesec_distance_learning'
BCRYPT_LOG_ROUNDS = 13

class Teacher():
    collection = db.users

    def __init__(self, _id=None, email="", password="", name="", subject=list(), contact="", profile_picture="avatar.svg",
    createdOn=datetime.now().strftime(dateFormat), updatedOn=datetime.now().strftime(dateFormat), createdBy=None,
    updatedBy=None,
    active=True, admin=False):
        self._id = _id
        self.email = email
        self.name = name
        self.admin = admin
        self.subject=subject
        self.profile_picture=profile_picture
        self.contact = contact
        self.password = password
        self.createdOn = createdOn
        self.updatedOn = updatedOn
        self.createdBy = createdBy
        self.active = active

    def save(self):
        user_data = self.to_json()
        user_data.pop("_id")
        self.collection.insert_one({**user_data, "password": self.password})

    def to_json(self):
        return {
            "_id": str(self._id),
            "email": self.email,
            "name": self.name,
            "admin": self.admin,
            "contact": self.contact,
            "profile_picture": self.profile_picture,
            "subject": self.subject,
            "createdOn": self.createdOn,
            "updatedOn": self.updatedOn,
            "createdBy": self.createdBy,
            "active": self.active
        }

    def encode_auth_token(user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(hours=3),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            import traceback
            traceback.print_exc()
            return e


    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, SECRET_KEY, algorithms=['HS256'])
            is_blacklisted_token = BlacklistToken().check_blacklist(auth_token)
            from pprint import pprint
            pprint(payload)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Session expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'