from datetime import datetime, timedelta
from google.appengine.ext import db
from helpers.db import HookedModel


class Entry(HookedModel):
    title = db.StringProperty(required=True)
    content = db.TextProperty()

    tags = db.StringListProperty()
    status = db.StringProperty(required=True, default='draft',
                               choices=['draft', 'published'])
    slug = db.StringProperty(required=True)

    created_at = db.DateTimeProperty(auto_now_add=True)
    updated_at = db.DateTimeProperty(auto_now=True)
    published_at = db.DateTimeProperty()

    def before_put(self):
      if self.status == 'published' and self.published_at is None:
        self.published_at = datetime.now()

    def is_updated(self):
      # add a second to self.published_at since Model stores
      # updated_at a few milliseconds after published_at
      return self.updated_at > (self.published_at + 
                                timedelta(seconds=1))

    # TODO:
    #  author