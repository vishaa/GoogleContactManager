from google.appengine.ext import ndb


class Contacts(ndb.Model):
    owner = ndb.StringProperty()
    name = ndb.StringProperty()
    name_lc = ndb.ComputedProperty(lambda self: self.name.lower())
    number = ndb.StringProperty(repeated=True)

    def to_dict(self):
        return {
            'id': self.key.id(),
            'name': self.name,
            'numbers': self.number
        }

    @staticmethod
    def add_contact(email, name, number):
        Contacts(owner=email, name=name, number=number).put()
