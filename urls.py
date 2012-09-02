from django.conf.urls.defaults import patterns, include

urlpatterns = patterns('',
    (r'', include('apps.blog.urls')),
    (r'hw/', include('core.urls')),
)
