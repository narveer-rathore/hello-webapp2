from google.appengine.ext import db


def category_key(category_name=None):
    return db.Key.from_path('Category', category_name)


def top_apps_key():
    return db.Key.from_path('TopApps', 'current')


def app_key(key=None):
    return db.Key.from_path('App', key)

def unic(t):
    return t.decode('UTF-8', 'replace') if isinstance(t, str) else t
