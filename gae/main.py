import webapp2

from handlers import CategoryHandler, CategoryGetHandler, AppDetailScraperHandler, TopAppsScraperHandler, TopAppsGetHandler
import json

from tasks import top_apps
# to run request modeule on GAE
from requests_toolbelt.adapters import appengine
appengine.monkeypatch()

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write('This is the RootHandler. Nothing to see here for now')

application = webapp2.WSGIApplication([
    webapp2.Route(r'/', handler=MainPage, name='root', methods=['GET']),

    webapp2.Route(r'/refresh', handler=top_apps, name='root_tasks', methods=['GET']),

    #bigquery
    webapp2.Route(r'/tasks/top', handler=TopAppsScraperHandler, name="top_category_scrapper", methods=['GET']),

    webapp2.Route(r'/top', handler=TopAppsGetHandler, name="top_category_apps", methods=['GET']),

    webapp2.Route(r'/app/<pkg>', handler=AppDetailScraperHandler, name="get_app", methods=['GET']),

    webapp2.Route(r'/category/add', handler=CategoryHandler, name="add_category", methods=['POST']),
    webapp2.Route(r'/category/<slug>/detail', handler=CategoryGetHandler, name="get_category", methods=['GET'])
], debug=True)


def main():
    application.run()


if __name__ == "__main__":
    main()
