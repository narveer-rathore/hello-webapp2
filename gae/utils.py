from google.appengine.ext import db

import requests
from bs4 import BeautifulSoup


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
