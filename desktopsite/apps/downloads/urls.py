from django.conf.urls.defaults import *
from desktopsite.apps.downloads.feeds import *

feeds = {
    'latest': LatestDownloads,
    'latest-stable': LatestStable,
    'latest-unstable': LatestUnstable,
}

urlpatterns = patterns('',
    url(r'^$', "desktopsite.apps.downloads.views.index", name="downloads-index"),
    url(r'^version.json$', "desktopsite.apps.downloads.views.version_ping"),
    url(r'^(?P<name>[\w\-\.]+)/$', "desktopsite.apps.downloads.views.release", name="downloads-release"),
    url(r'^(?P<release_name>[\w\-\.]+)/(?P<file_name>[\w\-\.]+)$', "desktopsite.apps.downloads.views.file"),
    # feeds
    url(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
)
