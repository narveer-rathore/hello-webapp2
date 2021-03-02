from google.appengine.ext import db
from datetime import datetime

class Category(db.Model):
    title = db.StringProperty()
    slug = db.StringProperty()
    view_order = db.IntegerProperty()
    more_link = db.LinkProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    groups = db.ListProperty(db.Key)

class App(db.Model):
    pkg = db.StringProperty(required=True)
    title = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    image = db.LinkProperty()
    review_count = db.IntegerProperty(default=0)
    rating = db.FloatProperty()
    developer = db.StringProperty()
    download_link = db.StringProperty()
    media = db.TextProperty()
    category = db.ReferenceProperty(Category, collection_name="category_apps")
    content_rating = db.StringProperty()
    content_rating_text = db.StringProperty()
    content_rating_image = db.TextProperty()
    description = db.TextProperty()
    screenshots = db.TextProperty()
    genre = db.StringProperty()
    rating = db.TextProperty()
    rating_count = db.TextProperty()
    last_fetched = db.DateTimeProperty(default=datetime.min)

class TopApps(db.Model):
    categories = db.ReferenceProperty(Category, collection_name="top_apps_in_categories")
    created = db.DateTimeProperty(auto_now_add=True)
