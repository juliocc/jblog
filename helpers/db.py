from google.appengine.ext import db

# Pre- and post- put hooks for Datastore models
# Taken from http://blog.notdot.net/2010/04/Pre--and-post--put-hooks-for-Datastore-models

class HookedModel(db.Model):
  def before_put(self):
    pass

  def after_put(self):
    pass

  def put(self, **kwargs):
    self.before_put()
    super(HookedModel, self).put(**kwargs)
    self.after_put()


old_put = db.put

def hooked_put(models, **kwargs):
  for model in models:
    if isinstance(model, HookedModel):
      model.before_put()
  old_put(models, **kwargs)
  for model in models:
    if isinstance(model, HookedModel):
      model.after_put()

db.put = hooked_put