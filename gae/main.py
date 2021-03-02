import webapp2

from handlers import CategoryHandler, CategoryGetHandler, AppDetailScraperHandler, TopAppsScraperHandler, TopAppsGetHandler
import json

# to run request modeule on GAE
from requests_toolbelt.adapters import appengine
appengine.monkeypatch()

import scrapper

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write('This is the RootHandler.')

application = webapp2.WSGIApplication([
    webapp2.Route(r'/', handler=MainPage, name='root', methods=['GET']),

    webapp2.Route(r'/top', handler=TopAppsGetHandler, name="top_category_apps", methods=['GET']),
    webapp2.Route(r'/top-scrapper', handler=TopAppsScraperHandler, name="top_category_scrapper", methods=['GET']),

    webapp2.Route(r'/app/<pkg>', handler=AppDetailScraperHandler, name="get_app", methods=['GET']),

    webapp2.Route(r'/category/add', handler=CategoryHandler, name="add_category", methods=['POST']),
    webapp2.Route(r'/category/<slug>/detail', handler=CategoryGetHandler, name="get_category", methods=['GET'])
], debug=True)


def main():
    application.run()


if __name__ == "__main__":
    main()
