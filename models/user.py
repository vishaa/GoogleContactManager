from google.appengine.ext import ndb

class User(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    picture = ndb.StringProperty()
    access_token = ndb.StringProperty(default="")
    refresh_token = ndb.StringProperty(default="")
    has_imported = ndb.BooleanProperty(default=True)

    @staticmethod
    def set_user(user_data):
        User(id=user_data.get('email'),
             name=user_data.get('name'),
             email=user_data.get('email'),
             picture=user_data.get('picture')).put()

    def set_token(self,token_data):
        self.access_token=token_data.get('access_token')
        self.refresh_token=token_data.get('refresh_token')
