import desktopsite.apps.desktopdocs.views
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(
        r'^$',
        desktopsite.apps.desktopdocs.views.index,
    ),
    url(
        r'^(?P<lang>[a-z-]+)/$',
        desktopsite.apps.desktopdocs.views.language,
    ),
    url(
        r'^(?P<lang>[a-z-]+)/(?P<version>[\w.-]+)/$',
        desktopsite.apps.desktopdocs.views.document,
        {'url': ''},
        name = 'document-index',
    ),
    url(
        r'^(?P<lang>[a-z-]+)/(?P<version>[\w.-]+)/search/$',
        desktopsite.apps.desktopdocs.views.search,
        name = 'document-search',
    ),
    url(
        r'^(?P<lang>[a-z-]+)/(?P<version>[\w.-]+)/_images/(?P<path>.*)$',
        desktopsite.apps.desktopdocs.views.images,
    ),
    url(
        r'^(?P<lang>[a-z-]+)/(?P<version>[\w.-]+)/_source/(?P<path>.*)$',
        desktopsite.apps.desktopdocs.views.source,
    ),
    url(
        r'^(?P<lang>[a-z-]+)/(?P<version>[\w.-]+)/(?P<url>[\w./-]*)/$',
        desktopsite.apps.desktopdocs.views.document,
        name = 'document-detail',
    ),
)
