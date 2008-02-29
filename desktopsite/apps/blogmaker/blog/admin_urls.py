''' Copyright (c) 2006-2007, PreFab Software Inc. '''


from django.conf.urls.defaults import patterns
from desktopsite.apps.blogmaker.blog.admin_views import entryRedirect, trackbacksRedirect


urlpatterns = patterns('',
    ('^(?P<id>\d+)/$', entryRedirect),
    ('^(?P<id>\d+)/postTrackbacks/$', trackbacksRedirect),
)

