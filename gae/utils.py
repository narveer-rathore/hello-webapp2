from google.appengine.ext import db

import requests
from bs4 import BeautifulSoup

from google.appengine.api import memcache


def category_key(category_name=None):
    return db.Key.from_path('Category', category_name)


def top_apps_key():
    return db.Key.from_path('TopApps', 'current')


def app_key(key=None):
    return db.Key.from_path('App', key)


def unic(t):
    return t.decode('UTF-8', 'replace') if isinstance(t, str) else t


def get_html(url):
    html_text = requests.get(url).text
    return BeautifulSoup(html_text, 'html.parser')


def print_stats(self):
    stats = memcache.get_stats()
    self.response.write('<b>Cache Hits:{}</b><br>'.format(stats['hits']))
    self.response.write('<b>Cache Misses:{}</b><br><br>'.format(stats['misses']))
