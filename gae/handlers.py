from __future__ import absolute_import

from datetime import datetime, timedelta

import webapp2
import json
import logging

from google.appengine.api import memcache
from models import Category, App

import scrapper
from utils import *
from serializers import serialize_app_list_item, serialize_category, serialize_app
from constants import SECONDS_IN_DAY

from google.cloud import bigquery

client = bigquery.Client()

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
        print(self.request.headers)

        if "X-Appengine-Cron" in self.request.headers:
            print("from cron")

        if "X-Appengine-Taskname" in self.request.headers:
            print("from task")

        res = scrapper.TopAppsScrapper(False)
        o = json.dumps(res)
        self.response.write(o)


class AppDetailScraperHandler(webapp2.RequestHandler):
    def get(self, pkg):
        #memcache

        try:
            res = memcache.get(pkg)
            # print_stats(self)
            source = "memcache"
            if res is None:
                obj = App.get_by_key_name(pkg)
                source = "db"
                if obj is None or (obj.last_fetched and obj.last_fetched + timedelta(days=1) < datetime.now()):
                    obj = scrapper.AppDetailScrapper(pkg, False)
                    source = "scrapper"

                res = serialize_app(obj)
                added = memcache.add(pkg, res, SECONDS_IN_DAY)

                if not added:
                    logging.error('Memcache set failed for app {}.'.format(pkg))

            self.response.headers['Content-Type'] = "application/json; charset=utf-8"
            o = json.dumps(res)
            ip = self.request.headers["X-Appengine-User-IP"] if X-Appengine-User-IP in self.request.headers else "0.0.0.0"
            q = """
                INSERT INTO 'hello-webapp2-1994.app_hits.app_detail'
                (app_id, request_date, source, country, ip, created_at)
                VALUES({}, {}, {}, {}, {}, {})
            """.format(pkg, datetime.now(), source, self.request.headers["X-Appengine-Country"], ip, datetime.now())

            query_job = client.query(q)
            print(query_job)
            self.response.write(o)

        except Exception as e:
            self.response.write(e)


class TopAppsGetHandler(webapp2.RequestHandler):
    def get(self):
        try:
            categories = memcache.get('categories')

            # print_stats(self)

            if categories is None:
                logging.info("memcache miss for categories")
                categoriesObj = Category.all()
                categories = []

                for cat in categoriesObj:
                    category = serialize_category(cat)
                    d = db.GqlQuery("SELECT * FROM App WHERE category = :1 ORDER by last_fetched limit 5", cat)
                    apps = []
                    for a in d:
                        apps.append(serialize_app_list_item(a))
                    category["apps"] = apps
                    categories.append(category)

                added = memcache.add("categories", categories, SECONDS_IN_DAY)

                if not added:
                    logging.error('Memcache set failed for categories.')

        except Exception as e:
            self.response.write(e)

        self.response.write({
            "data": categories
        })
