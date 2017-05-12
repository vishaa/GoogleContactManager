from uuid import uuid4
from google.appengine.ext import ndb

class Session(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()

    @staticmethod
    def set_session(user_data):
        uuid = str(uuid4())
        Session(id=uuid,
                         name=user_data.get('name'),
                         email=user_data.get('email')).put()
        return uuid
