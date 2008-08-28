from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', "desktopsite.apps.content.views.index", name="content-index"),
)
