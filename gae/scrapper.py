import logging
import json

import re
import requests
import urlparse

from serializers import serialize_app
from datetime import datetime, timedelta
from constants import TOP_APPS_URL, APP_DETAIL_URL, STORE_URL
from utils import get_html

def TopAppsScrapper(test):
  logging.info("Starting app scrapper")

  try:
    soup = get_html(TOP_APPS_URL)
  except Exception as e:
    return e

  items = soup.find(attrs={"jsdata": "deferred-i7"})

  attributes_to_del = ["data-p", "js-action", "style", "jsdata", "jslog"]

  for attr_del in attributes_to_del:
    [s.attrs.pop(attr_del) for s in soup.find_all() if attr_del in s.attrs]

  categories = []
  for index, cat in enumerate(items):
    if cat.name == "c-wiz":
      category = {}
      category["apps"] = []
      category["view_order"] = index
      try:
        main = cat.div
        header = main.findChild().findChild().find("a")
        category["title"] = header.find("h2").text
        category["more_link"] = header["href"]

        category["slug"] = category["title"].lower().replace(" ", "_")
        child = main.contents[1].select("c-wiz > div > div")
        for c in child:
          div = c.contents[1]
          pkg = {}
          image = c.find("img")["data-src"]

          if image and "image" not in pkg:
            pkg["image"] = image

          pkg["title"] = div.select("[title]")[0].text.encode('utf-8').strip()
          links = div.select("[href]")

          for l in links:
            url = urlparse.urlparse(l["href"])

            if url.path.startswith("/store/apps/details"):
              if not "package" in pkg:
                pkg["download_link"] = l["href"]
                pkg["package"] = url.query[3:].encode('utf-8').strip()


            if url.path.startswith("/store/apps/developer"):
              if not "developer" in pkg:
                pkg["developer"] = url.query[3:].replace("+", " ").encode('utf-8').strip()

            des = l.find('div')
            if not l.find('div'):
              if l.text:
                pkg["description"] = l.text.encode('utf-8').strip()

          category["apps"].append(pkg)

      except Exception as e:
        return e

      categories.append(category)

      logging.info("\nFor category {} got {} apps".format(category["title"], len(category["apps"])))


  logging.info("Done getting data from scrapper ")

  if not test:
    from models import Category, App
    from utils import unic, app_key, category_key

    try:
      for c in categories:
        slug = unic(c["slug"])
        key = category_key(slug)

        cat = Category.get_by_key_name(slug)

        if not cat:
          cat = Category(key=key, slug=slug, title=c["title"])
          cat.view_order = c["view_order"]
          cat.more_link = STORE_URL.format(c.get("more_link", ""))
          cat.put()

        for app in c["apps"]:
          name = app["package"]
          obj = App.get_or_insert(name, pkg=name)
          obj.category = cat
          obj.key = app_key(name)
          obj.pkg = unic(name)
          obj.title = unic(app["title"])
          obj.image = app.get("image", None)
          obj.download_link = app.get("download_link", None)
          obj.developer = unic(app.get("developer", None))
          obj.put()

    except Exception as e:
      logging.error(e)
      return e
    else:
      return categories


def AppDetailScrapper(pkg, test):
  url = APP_DETAIL_URL.format(pkg)

  try:
    soup = get_html(url)
  except Exception as e:
    return e

  main = soup.find('main')

  try:
    rating = soup.find_all("div", {"aria-label": re.compile(" stars out of five stars$")})[0]["aria-label"]
    rating = rating.split(" ")[1]
    rating_count = soup.find_all("span", {"aria-label": re.compile(" ratings$")})[0]["aria-label"]
    rating_count = rating_count.split(" ")[0]
  except:
    rating = ""
    rating_count = 0

  genre = main.select('[itemprop="genre"]')[0].text

  screenshots = [x.find("img") for x in main.select('[data-screenshot-item-index]') if x]
  screenshots = map(lambda x: x.get("srcset") and x.get("srcset").split(" ")[0], screenshots)

  description = " ".join([ x.text for x in main.select('[itemprop="description"]') if x.text]).encode('utf-8').strip()

  if not test:
    from models import App
    from utils import unic, app_key

    obj = App.get_or_insert(pkg, pkg=pkg)
    obj.key = app_key(pkg)
    obj.rating = rating
    obj.rating_count = rating_count
    obj.genre = genre
    obj.screenshots = json.dumps(screenshots)
    obj.description = unic(description)
    obj.last_fetched = datetime.now()
    obj.put()
    logging.info("saved new app data {} for {}".format(pkg, obj.last_fetched.strftime("%Y-%m-%d %H:%M:%S")))
    return { "success": "fetching ", "date": obj.last_fetched.strftime("%Y-%m-%d %H:%M:%S"), "data": serialize_app(obj) }

  return pkg

def main():
  Scrapper(True)
  AppDetailScrapper("com.next.innovation.takatak.lite", True)

if __name__ == "__main__":
  main()
