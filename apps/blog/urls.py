from django.conf.urls.defaults import patterns, url

from apps.blog.views import (BlogIndex, AllIndex, TagView, EntryView, 
                             entry_create, entry_delete)

urlpatterns = patterns('',
    # Diagnosis urls...
    url(r'^entries/$', BlogIndex.as_view(), name='blog_index'),
    url(r'^entries/create/$', entry_create, name='entry_create'),
    url(r'^entries/all/$', AllIndex.as_view(), name='all_index'),
    url(r'^entries/(?P<slug>[\w\d_-]+)/$', EntryView.as_view(), name='entry_view'),
    url(r'^entries/(?P<slug>[\w\d_-]+)/edit/$', entry_create, name='entry_edit'),
    url(r'^entries/(?P<slug>[\w\d_-]+)/delete/$', entry_delete, name='entry_delete'),

    url(r'^tag/(?P<tag>[\w _-]+)/$', TagView.as_view(), name='tag_index'),
)
