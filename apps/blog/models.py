import random
from datetime import datetime, timedelta
import re

from django.template.defaultfilters import slugify, truncatewords_html
from google.appengine.ext import db
from helpers.db import HookedModel            

class Entry(HookedModel):
    title = db.StringProperty(required=True)
    content = db.TextProperty()
    author = db.UserProperty(auto_current_user_add=True)
    tags = db.ListProperty(db.Key) # references to Tag
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

class Tag(db.Model):
    title = db.StringProperty(required=True)
    count = db.IntegerProperty(default=1)

    @classmethod
    def inc_or_insert(cls, title):
        def txn(title):
            tag = cls.get_by_key_name(title, parent=None)
            if tag:
                tag.count += 1
            else:
                tag = cls(key_name=title, title=title)
            tag.put()
            return tag

        return db.run_in_transaction(txn, title=title)

    @classmethod
    def inc_or_insert(cls, title):
        def txn(title):
            tag = cls.get_by_key_name(title, parent=None)
            if tag:
                tag.count += 1
            else:
                tag = cls(key_name=title, title=title)
            tag.put()
            return tag

        return db.run_in_transaction(txn, title=title)

    @classmethod
    def try_dec(cls, title):
        def txn(title):
            tag = cls.get_by_key_name(title, parent=None)
            if tag:
                tag.count -= 1
                tag.put()
                return tag
            return None

        return db.run_in_transaction(txn, title=title)


    @classmethod
    def cloud(cls):
        tags = cls.all().order('-count').fetch(25)
        max = None
        for tag in tags:
            if tag.count > max or max is None:
                max = tag.count

        NUM_BUCKETS = 4.0
        buckets = []
        for tag in tags:
            buckets.append(int((tag.count/float(max) * NUM_BUCKETS) + 0.5) )
            
        cloud = zip(buckets, tags)
        # random but consistent sort
        cloud.sort(key=lambda x: hash(x[1].key()))
        return cloud