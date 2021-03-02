import webapp2
import json

from models import Category, App
from utils import *
from serializers import serialize_app_list_item, serialize_category
class CategoryHandler(webapp2.RequestHandler):
    def post(self):
        try:
            data = json.loads(self.request.body)
            slug = data['slug']

            if not slug:
                raise Exception("Slug is required.")

            category = Category.get_by_key_name(slug)

            if category:
                raise Exception("Category already exists for slug '{}'.".format(slug))
            else:
                category = Category(key=category_key(slug), title=data['title'], slug=data['slug'])
                category.put()
                self.response.write(json.dumps({
                    "msg": "Success " + category.title,
                    "slug": slug
                }))
        except Exception as e:
            self.response.write(str(e))


class CategoryGetHandler(webapp2.RequestHandler):
    def get(self, slug):
        try:
            if not slug:
                raise Exception("Slug is required.")

            category = Category.get_by_key_name(slug)

            if not category:
                raise Exception("Category not found")
            else:
                self.response.write(json.dumps({
                    "slug": category.slug,
                    "title": category.title
                }))

        except Exception as e:
            self.response.write(str(e))


class TopAppsScraperHandler(webapp2.RequestHandler):
    def get(self):
        res = scrapper.TopAppsScrapper(False)
        self.response.write(json.dumps(res))


class AppDetailScraperHandler(webapp2.RequestHandler):
    def get(self, pkg):
        res = scrapper.AppDetailScrapper(pkg, False)
        self.response.write(json.dumps(res))


class TopAppsGetHandler(webapp2.RequestHandler):
    def get(self):
        categories = Category.all()

        response = []

        for cat in categories:
            category = serialize_category(cat)
            d = db.GqlQuery("SELECT * FROM App WHERE category = :1 ORDER by last_fetched limit 5 ", cat)
            # data = App.gql("category_apps = 'com.fingersoft.hillclimb'").get()
            apps = []
            for a in d:
                apps.append(serialize_app_list_item(a))
            category["apps"] = apps
            response.append(category)

        self.response.write({
            "data": response
        })


