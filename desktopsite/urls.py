from django.conf.urls.defaults import *
from desktopsite.apps.blog.feeds import WeblogEntryFeed
from django.contrib.comments.feeds import LatestFreeCommentsFeed
from desktopsite.settings import ROOT_PATH
from django.contrib import admin
admin.autodiscover()

feeds = {
     'weblog': WeblogEntryFeed,
     'comments': LatestFreeCommentsFeed,
}

urlpatterns = patterns('',
    (r'^forum/', include('desktopsite.apps.snapboard.urls')),
    (r'^blog/', include('desktopsite.apps.blog.urls')),
    (r'^repository/', include('desktopsite.apps.repository.urls')),
    (r'^dojango/', include('dojango.urls')),
    (r'^rss/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
    ### TEMPORARY, REMOVE IN PRODUCTION SITE ###
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '%s/media' % ROOT_PATH}),
    
    (r'^admin/(.*)', admin.site.root),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'', include('desktopsite.apps.accounts.urls')),
    (r'', include('desktopsite.apps.content.urls')),
    (r'', include('django.contrib.flatpages.urls')),
)
