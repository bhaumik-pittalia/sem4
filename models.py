from google.appengine.ext import ndb
from google.appengine.api import users

class Resource(ndb.Model):
    name = ndb.StringProperty(indexed=True)
    email = ndb.StringProperty()
    phone = ndb.IntegerProperty(indexed=True)
    address = ndb.StringProperty(indexed=True)

    def browse(self,urlsafe):
        return ndb.Key(urlsafe=urlsafe).get()

class Schedule(ndb.Model):
    resource = ndb.KeyProperty(kind=Resource)
    day = ndb.StringProperty(indexed=True)
    time_from = ndb.TimeProperty(indexed=True)
    time_to = ndb.TimeProperty(indexed=True)

class Appointment(ndb.Model):
    resource = ndb.KeyProperty(kind=Resource)
    date = ndb.DateProperty(indexed=True)
    time_from = ndb.TimeProperty(indexed=True)
    time_to = ndb.TimeProperty(indexed=True)
    name = ndb.StringProperty(indexed=True)
    phone = ndb.IntegerProperty(indexed=True)
    email = ndb.StringProperty(indexed=True)