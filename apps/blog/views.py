from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import TemplateView

from apps.blog.models import Entry
from helpers.paginator import GAEPaginator

class BlogIndex(TemplateView):
  http_method_names = ['get']
  template_name = 'blog/index.html'

  def get_context_data(self, **kwargs):
    context = super(BlogIndex, self).get_context_data(**kwargs)
    query = Entry.all().filter('status =', 'published') \
                 .order('-published_at')
    paginator = GAEPaginator(query, 10)
  
    try:
      entries = paginator.page(self.request.GET.get('page', '1'))
    except PageNotAnInteger:
      entries = paginator.page(1)
    except EmptyPage:
      entries = paginator.page(paginator.num_pages)

    context['entries'] = entries
    return context