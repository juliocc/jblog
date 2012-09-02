from django.conf.urls.defaults import patterns, url

from apps.blog.views import BlogIndex

urlpatterns = patterns('',
    # Diagnosis urls...
    url(r'^$', BlogIndex.as_view(), name='blog_index'),
)
