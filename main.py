
# Users
from google.appengine.api import users
import webapp2

class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.out.write('Hello, ' + user.nickname())
        else:
            self.redirect(users.create_login_url(self.request.uri))

application = webapp2.WSGIApplication([
    ('/', MainPage)
], debug=True)

def main():
    application.run()

if __name__ == "__main__":
    main()




# Hello, world ;)

# import webapp2

# class MainPage(webapp2.RequestHandler):
#     def get(self):
#         self.response.headers['Content-Type'] = 'text/plain'
#         self.response.out.write('Hello, webapp2 World test!')
#         self.response.out.write(self.request)

# app = webapp2.WSGIApplication([
#     ('/', MainPage)
# ], debug=True)
