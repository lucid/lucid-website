from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', "desktopsite.apps.content.views.index"),
)
