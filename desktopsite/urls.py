from django.conf.urls.defaults import *
from desktopsite.apps.blog.feeds import WeblogEntryFeed
from django.contrib.comments.feeds import LatestFreeCommentsFeed
from desktopsite.settings import ROOT_PATH

feeds = {
     'weblog': WeblogEntryFeed,
     'comments': LatestFreeCommentsFeed,
}

urlpatterns = patterns('',
    (r'^forum/', include('desktopsite.apps.snapboard.urls')),
    (r'^blog/', include('desktopsite.apps.blog.urls')),
    (r'^dojango/', include('dojango.urls')),
    (r'^rss/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
    ### TEMPORARY, REMOVE IN PRODUCTION SITE ###
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '%s/media' % ROOT_PATH}),
    
    (r'^admin/', include('django.contrib.admin.urls')),
    (r'', include('desktopsite.apps.accounts.urls')),
    (r'', include('desktopsite.apps.content.urls')),
    (r'', include('django.contrib.flatpages.urls')),
)
