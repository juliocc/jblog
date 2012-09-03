from django.conf.urls.defaults import patterns, url

from apps.blog.views import BlogIndex, AllIndex, TagView, EntryView, entry_create

urlpatterns = patterns('',
    # Diagnosis urls...
    url(r'^$', BlogIndex.as_view(), name='blog_index'),
    url(r'^all/$', AllIndex.as_view(), name='all_index'),
                       url(r'^tag/(?P<tag>[\w _-]+)/$', TagView.as_view(), name='tag_index'),
    url(r'^entries/(?P<slug>[\w\d_-]+)/$', EntryView.as_view(), name='entry_view'),
    url(r'^post/$', entry_create, name='entry_create'),
    url(r'^edit/(?P<slug>[\w\d_-]+)/$', entry_create, name='entry_edit'),
)
