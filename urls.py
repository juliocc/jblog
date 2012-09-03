from django.conf.urls.defaults import patterns, include, url
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse
from django.utils.functional import lazy

reverse_lazy = lazy(reverse, str)


urlpatterns = patterns('',
    url(r'$^', RedirectView.as_view(url=reverse_lazy('blog_index')), name='home'),
    (r'', include('apps.blog.urls')),
)
