from setup import db, dateFormat
from datetime import datetime

class BlacklistToken():
    """
    Token Model for storing JWT tokens
    """
    collection = db.blacklist_token

    def __init__(self, _id=None, token="", blacklistedOn=datetime.now().strftime(dateFormat)):
        self._id = _id
        self.token = token
        self.blacklistedOn = blacklistedOn

    def save(self):
        self.collection.insert_one(self.to_json())

    def to_json(self):
        return {
            "id": self._id,
            "token": self.token,
            "blacklistedOn": self.blacklistedOn,
        }

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    def check_blacklist(self, auth_token):
        # check whether auth token has been blacklisted
        res = self.collection.find_one(dict(token=str(auth_token)))
        if res:
            return True
        else:
            return False