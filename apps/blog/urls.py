from django.conf.urls.defaults import patterns, url

from apps.blog.views import BlogIndex, TagView, EntryView

urlpatterns = patterns('',
    # Diagnosis urls...
    url(r'^$', BlogIndex.as_view(), name='blog_index'),
    url(r'^tag/(?P<tag>\w+)/$', TagView.as_view(), name='tag_index'),
    url(r'^entries/(?P<slug>\w+)/$', EntryView.as_view(), name='entry_view'),
)
