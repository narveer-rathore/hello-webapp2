def serialize_app(app):
  return {
    "title": app.title.decode('utf-8').strip(),
    "pkg": app.pkg,
    "rating": app.rating,
    "image": app.image,
    "last_fetched": app.last_fetched.strftime("%Y-%m-%d %H:%M:%S"),
    "description": app.description.decode('utf-8').strip()
  }

def serialize_category(app):
  return {
    "slug": app.slug.decode('utf-8').strip(),
    "title": app.title.decode('utf-8'),
    "view_order": app.view_order,
    "more_link": app.more_link,
  }

def serialize_app_list_item(app):
  return {
    "title": app.title,
    "pkg": app.pkg,
    "image": app.image,
  }
