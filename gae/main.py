import cgi
import datetime
import time
import urllib
import wsgiref.handlers
import logging

from google.appengine.ext import db
from google.appengine.api import users
import webapp2

import json

from models import Category

SIMPLE_TYPES = (int, long, float, bool, dict, basestring, list)


def to_dict(model):
    output = {}

    for key, prop in model.properties().iteritems():
        value = getattr(model, key)

        if value is None or isinstance(value, SIMPLE_TYPES):
            output[key] = value
        elif isinstance(value, datetime.date):
            # Convert date/datetime to MILLISECONDS-since-epoch (JS "new Date()").
            ms = time.mktime(value.utctimetuple()) * 1000
            ms += getattr(value, 'microseconds', 0) / 1000
            output[key] = int(ms)
        elif isinstance(value, db.GeoPt):
            output[key] = {'lat': value.lat, 'lon': value.lon}
        elif isinstance(value, db.Model):
            output[key] = to_dict(value)
        else:
            raise ValueError('cannot encode ' + repr(prop))

    return output


def category_key(category_name=None):
    return db.Key.from_path('Category', category_name)


def top_apps_key():
    return db.Key.from_path('TopApps', 'current')


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write('This is the HomeHandler.')

class HomeHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('This is the HomeHandler.')

class CategoryHandler(webapp2.RedirectHandler):
    def post(self):
        data = json.loads(self.request.body)
        print(data['category_name'])
        category = Category(title=data['title'], slug=data['slug'])
        category.put()
        self.response.write("Success " + category.title)

    def get(self):
        try:
            categories = db.GqlQuery("SELECT * "
                                    "FROM Category "
                                    "WHERE ANCESTOR IS :1 "
                                    "ORDER BY created DESC LIMIT 10")

            self.response.write(categories.count())

        except e:
            logging.debug(str(e))


application = webapp2.WSGIApplication([
    webapp2.Route(r'/', handler=HomeHandler, name='home'),
    webapp2.Route(r'/top', handler=MainPage, name='main'),
    webapp2.Route(r'/category', handler=CategoryHandler, name="category")
], debug=True)


def main():
    application.run()


if __name__ == "__main__":
    main()
