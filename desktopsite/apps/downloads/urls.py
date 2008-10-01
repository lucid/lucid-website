from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', "desktopsite.apps.downloads.views.index", name="downloads-index"),
    url(r'^version.json$', "desktopsite.apps.downloads.views.version_ping"),
    url(r'^(?P<name>[\w\-\.]+)/$', "desktopsite.apps.downloads.views.release", name="downloads-release"),
    url(r'^(?P<release_name>[\w\-\.]+)/(?P<file_name>[\w\-\.]+)$', "desktopsite.apps.downloads.views.file"),
)
