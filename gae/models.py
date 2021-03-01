from google.appengine.ext import db
from google.appengine.api import users
import webapp2

class Category(db.Model):
    title = db.StringProperty(required=True)
    slug = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)

class TopApps(db.Model):
    category = db.StringProperty()
    apps = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add=True)

class App(db.Model):
    title = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    image = db.StringProperty()
    review_count = db.IntegerProperty()
    rating = db.FloatProperty()
    developer = db.StringProperty()
    app_type = db.StringProperty()
    download_link = db.StringProperty()
    media = db.StringProperty()
    category = db.StringProperty()
