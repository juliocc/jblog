import random
from datetime import datetime, timedelta
import re

from django.template.defaultfilters import slugify, truncatewords_html
from google.appengine.ext import db
from helpers.db import HookedModel

tag_re = re.compile('[^\w _-]')
class TagListProperty(db.StringListProperty):
    def validate(self, value):
        # tags should only contain leters, numbers, whitespace and dashes
        value = super(TagListProperty, self).validate(value)
        for tag in value:
            if tag_re.search(tag):
                raise db.BadValueError('tags should only contain letters, '
                                       'numbers, whitespace and dashes')

        return value
            
        

class Entry(HookedModel):
    title = db.StringProperty(required=True)
    content = db.TextProperty()
    author = db.UserProperty(auto_current_user_add=True)
    tags = TagListProperty()
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
                # 'create' and 'all' are special urls, avoid using them as slugs
                if not exists and slug not in ('create', 'all'):
                    break

                extra = extra + "-" + str(random.randrange(100))
                
            self.slug = slug
            

    def is_updated(self):
        # add a second to self.published_at since Model stores
        # updated_at a few milliseconds after published_at
        return self.updated_at > (self.published_at + 
                                  timedelta(seconds=1))

    @property
    def excerpt(self):
        parts = self.content.split('<!--more-->', 1)
        if len(parts) == 1:
            return truncatewords_html(parts[0], 40)
        return parts[0]

    # TODO:
    #  author