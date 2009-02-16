import desktopdocs.views
from django.conf.urls.defaults import *

prefix = "documentation/"

urlpatterns = patterns('',
    url(
        r'^%s$' % prefix,
        desktopdocs.views.index,
    ),
    url(
        r'^%s(?P<lang>[a-z-]+)/$' % prefix,
        desktopdocs.views.language,
    ),
    url(
        r'^%s(?P<lang>[a-z-]+)/(?P<version>[\w.-]+)/$' % prefix,
        desktopdocs.views.document,
        {'url': ''},
        name = 'document-index',
    ),
    url(
        r'^%s(?P<lang>[a-z-]+)/(?P<version>[\w.-]+)/search/$' % prefix,
        desktopdocs.views.search,
        name = 'document-search',
    ),
    url(
        r'^%s(?P<lang>[a-z-]+)/(?P<version>[\w.-]+)/_images/(?P<path>.*)$' % prefix,
        desktopdocs.views.images,
    ),
    url(
        r'^%s(?P<lang>[a-z-]+)/(?P<version>[\w.-]+)/_source/(?P<path>.*)$' % prefix,
        desktopdocs.views.source,
    ),
    url(
        r'^%s(?P<lang>[a-z-]+)/(?P<version>[\w.-]+)/(?P<url>[\w./-]*)/$' % prefix,
        desktopdocs.views.document,
        name = 'document-detail',
    ),
)
