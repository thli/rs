from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'rsgraphs.views.redirect_to_index'),
    url(r'^index$', 'rsgraphs.views.index', name='index'),
    url(r'^graph/(?P<item_name>.+)', 'rsgraphs.views.graph', name='graph'),
)