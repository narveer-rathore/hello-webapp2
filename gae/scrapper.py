import cgi
import datetime
import urllib
import wsgiref.handlers

from google.appengine.ext import db
from google.appengine.api import users
import webapp2

class App(db.Model):
    title = db.StringProperty()
    created_at = db.DateTimeProperty(auto_now_add=True)
    imgPath = db.StringProperty()
    review_count = db.In



class Greeting(db.Model):
  """Models an individual Guestbook entry with an author, content, and date."""
  author = db.UserProperty()
  content = db.StringProperty(multiline=True)
  date = db.DateTimeProperty(auto_now_add=True)


def guestbook_key(guestbook_name=None):
  """Constructs a datastore key for a Guestbook entity with guestbook_name."""
  return db.Key.from_path('Guestbook', guestbook_name or 'default_guestbook')


class MainScrapper(webapp2.RequestHandler):
  def get(self):



application = webapp2.WSGIApplication([
  ('/', MainScrapper),
], debug=True)

def main():
    application.run()

if __name__ == "__main__":
    main()
