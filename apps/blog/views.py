from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import TemplateView

from apps.blog.models import Entry
from helpers.paginator import GAEPaginator

class EntriesView(TemplateView):
    http_method_names = ['get']
    template_name = 'blog/index.html'

    def get_page(self, query):
        paginator = GAEPaginator(query, 10)
        try:
            entries = paginator.page(self.request.GET.get('page', '1'))
        except PageNotAnInteger:
            entries = paginator.page(1)
        except EmptyPage:
            entries = paginator.page(paginator.num_pages)

        return entries

    def get_context_data(self, **kwargs):
        context = super(EntriesView, self).get_context_data(**kwargs)
        entries = self.get_page(self.get_query())
        context['entries'] = entries
        return context
      

class BlogIndex(EntriesView):
    def get_query(self):
        return Entry.all().filter('status =', 'published') \
                          .order('-published_at')


class TagView(EntriesView):
    def get_query(self):
        return Entry.all().filter('status =', 'published') \
                          .filter('tags =', self.kwargs['tag']) \
                          .order('-published_at')

class EntryView(TemplateView):
    template_name = 'blog/view.html'

    def get_context_data(self, **kwargs):
        context = super(EntryView, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        entry = Entry.all().filter('slug =', slug).get()
        # TODO: handle no results
        context['entry'] = entry
        return context