from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', "desktopsite.apps.repository.views.index"),
    (r'^letter/(?P<letter>[A-Z])/$', "desktopsite.apps.repository.views.byLetter"),
    (r'^category/(?P<category>.+)/$', "desktopsite.apps.repository.views.byCategory"),
    (r'^search/$', "desktopsite.apps.repository.views.search"),
    (r'^packages/(?P<sysname>[\w-]+)/$', "desktopsite.apps.repository.views.package"),
    (r'^packages/(?P<sysname>[\w-]+)/newversion/$', "desktopsite.apps.repository.views.newVersion"),
    (r'^packages/(?P<sysname>[\w-]+)/(?P<version>.+)/$', "desktopsite.apps.repository.views.version"),
    
    (r'^vote/$', "desktopsite.apps.repository.views.saveRating"),
    (r'^newpackage/$', "desktopsite.apps.repository.views.newPackage"),
    (r'^mypackages/$', "desktopsite.apps.repository.views.userPackages"),
)
