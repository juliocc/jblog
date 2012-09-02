from django.views.generic import TemplateView
from apps.blog.models import Entry

class BlogIndex(TemplateView):
  http_method_names = ['get']
  template_name = 'blog/index.html'

  def get_context_data(self, **kwargs):
    context = super(BlogIndex, self).get_context_data(**kwargs)
    context['entries'] = Entry.all().order('-created_at').fetch(limit=10)
    return context