from google.appengine.ext import ndb


class Contacts(ndb.Model):
    owner = ndb.StringProperty()
    name = ndb.StringProperty()
    number = ndb.StringProperty(repeated=True)

    @staticmethod
    def add_contact(email, name, number):
        Contacts(owner=email, name=name, number=number).put()
