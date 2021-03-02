from scrapper import TopAppsScrapper
from google.appengine.api import taskqueue

import webapp2
import logging

from datetime import datetime


class top_apps(webapp2.RequestHandler):
  def get(self):
    logging.info("Starting task for refreshing apps ")
    taskqueue.add(
        method='GET',
        queue_name='queue-blue',
        url='/tasks/top',
        name='refresh-' + datetime.today().strftime("%Y-%m-%d")
    )
