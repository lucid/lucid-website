from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', "desktopsite.apps.content.views.index", name="content-index"),
    url(r'^search/$', "desktopsite.apps.content.views.search", name="search"),
)
