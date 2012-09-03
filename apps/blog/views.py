from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import TemplateView
from django.views.generic import CreateView
from django.template import RequestContext
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.utils import simplejson
from django.http import HttpResponse, Http404
from google.appengine.api import users

from helpers.paginator import GAEPaginator
from apps.blog.models import Entry, Tag
from apps.blog.forms import EntryForm

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
        context['cloud'] = Tag.cloud()
        return context
      

class BlogIndex(EntriesView):
    def get_query(self):
        return Entry.all().filter('status =', 'published') \
                          .order('-published_at')

class AllIndex(EntriesView):
    def get_query(self):
        return Entry.all().order('-created_at')

class TagView(EntriesView):
    def get_query(self):
        tag = Tag.get_by_key_name(self.kwargs['tag'])
        return Entry.all().filter('status =', 'published') \
                          .filter('tags =', tag.key()) \
                          .order('-published_at')
  

class EntryView(TemplateView):
    template_name = 'blog/view.html'

    def get_context_data(self, **kwargs):
        context = super(EntryView, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        entry = Entry.all().filter('slug =', slug).get()
        if not entry:
            raise Http404

        context['entry'] = entry
        return context


class HttpTextResponse(HttpResponse):
    def __init__(self, *args, **kwargs):
        kwargs['content_type'] = 'text/plain; charset=utf-8'
        super(HttpTextResponse, self).__init__(*args, **kwargs)

def admin_required(func):
    """Decorator that insists that you're logged in as administratior."""

    def admin_wrapper(request, *args, **kwds):
        if request.user is None:
            return redirect(
                users.create_login_url(request.get_full_path().encode('utf-8')))
        if not request.user_is_admin:
            return HttpTextResponse(
                'You must be admin for this function', status=403)
        return func(request, *args, **kwds)

    return admin_wrapper

@admin_required
def entry_create(request, slug=None):
    if slug is not None:
        entry = Entry.all().filter('slug =', slug).get()
        action_url = reverse('entry_edit', args=[slug])
        initial = {'title': entry.title,
                   'content': entry.content,
                   'tags': "\n".join(tag.name() for tag in entry.tags),
                   'status': entry.status}
    else:
        entry = None
        action_url = reverse('entry_create')
        initial = None

    if request.method == 'POST':
        form = EntryForm(request.POST, initial)
        if form.is_valid():
            if not initial:
                tags = []
                for tagtitle in form.cleaned_data['tags']:
                    tag = Tag.inc_or_insert(tagtitle)
                    tags.append(tag.key())
                form.cleaned_data['tags'] = tags
                
                entry = Entry(**form.cleaned_data)
                entry.put()
                messages.success(request, 'Post created successfully')
            else:
                initial_tags = [tag.name() for tag in entry.tags]
                new_tags = form.cleaned_data['tags']

                new = set(new_tags) - set(initial_tags)
                existing = set(new_tags) & set(initial_tags)
                deleted = set(initial_tags) - set(new_tags)

                tags = []
                for tagtitle in deleted:
                    Tag.try_dec(tagtitle)

                for tagtitle in new_tags:
                    if tagtitle in new:
                        tag = Tag.inc_or_insert(tagtitle)
                        tags.append(tag.key())
                    elif tagtitle in existing:
                        tag = Tag.get_by_key_name(tagtitle)
                        tags.append(tag.key())
                    else:
                        raise Exception("what?")

                entry.tags = tags
                entry.title = form.cleaned_data['title']
                entry.status = form.cleaned_data['status']
                entry.content = form.cleaned_data['content']
                entry.put()
                messages.success(request, 'Post modified successfully')
                
            if entry.status == 'draft':
                msg = ('<strong>Warning</strong> The post was saved as a '
                       'draft and will not be visisble from the homepage. '
                       'Click <a href="%s">here</a> to view all your posts.'
                       % reverse('all_index'))
                messages.warning(request, mark_safe(msg))
            
            return redirect('entry_view', entry.slug)
    else:
        form = EntryForm(initial)

    return render_to_response('blog/create.html', {
        'form': form,
        'action_url': action_url
        },
        context_instance=RequestContext(request))


@require_POST
@admin_required
def entry_delete(request, slug=None):
    data = {}
    if slug is None:
        raise Http404

    entry = Entry.all().filter('slug =', slug).get()
    if not entry:
        raise Http404

    entry.delete()
    messages.warning(request, 'Entry deleted')
    data['redirect_url'] = reverse('blog_index')

    return HttpResponse(simplejson.dumps(data), 
                        mimetype="application/json")


def context_processor(request):
    params = {}
    full_path = request.get_full_path().encode('utf-8')
    user = users.get_current_user()
    if user is None:
        params['login_url'] = users.create_login_url(full_path)
    else:
        params['logout_url'] = users.create_logout_url(full_path)
    return params
