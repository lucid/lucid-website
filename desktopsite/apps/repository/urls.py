from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', "desktopsite.apps.repository.views.index"),
    (r'^letter/(?P<letter>\d+)/$', "desktopsite.apps.repository.views.byLetter"),
    (r'^category/(?P<category>\d+)/$', "desktopsite.apps.repository.views.byCategory"),
    (r'^search/$', "desktopsite.apps.repository.views.search"),
)
