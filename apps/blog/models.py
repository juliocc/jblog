import random
from datetime import datetime, timedelta

from django.template.defaultfilters import slugify
from google.appengine.ext import db
from helpers.db import HookedModel


class Entry(HookedModel):
    title = db.StringProperty(required=True)
    content = db.TextProperty()

    tags = db.StringListProperty()
    status = db.StringProperty(required=True, default='draft',
                               choices=['draft', 'published'])
    slug = db.StringProperty()

    created_at = db.DateTimeProperty(auto_now_add=True)
    updated_at = db.DateTimeProperty(auto_now=True)
    published_at = db.DateTimeProperty()

    def before_put(self):
        if self.status == 'published' and self.published_at is None:
            self.published_at = datetime.now()

        # create a unique slug
        if not self.is_saved():
            extra = self.title
            while 1:
                slug = str(slugify(extra))
                exists = Entry.all(keys_only=True).filter('slug =', slug).fetch(limit=1)
                if not exists:
                    break

                extra = extra + "-" + str(random.randrange(100))
                
            self.slug = slug
            

    def is_updated(self):
        # add a second to self.published_at since Model stores
        # updated_at a few milliseconds after published_at
        return self.updated_at > (self.published_at + 
                                  timedelta(seconds=1))

    # TODO:
    #  author