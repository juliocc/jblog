from google.appengine.ext import db

class Entry(db.Model):
    title = db.StringProperty(required=True)
    content = db.TextProperty()

    tags = db.StringListProperty()
    # status = 
    slug = db.StringProperty()

    created_at = db.DateTimeProperty(auto_now_add=True)
    updated_at = db.DateTimeProperty(auto_now=True)
    # published_at = db.DateTimeProperty()

    # TODO:
    # add status, published_at and author