import desktopdocs.views
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(
        r'^$',
        desktopdocs.views.index,
    ),
    url(
        r'^(?P<lang>[a-z-]+)/$',
        desktopdocs.views.language,
    ),
    url(
        r'^(?P<lang>[a-z-]+)/(?P<version>[\w.-]+)/$',
        desktopdocs.views.document,
        {'url': ''},
        name = 'document-index',
    ),
    url(
        r'^(?P<lang>[a-z-]+)/(?P<version>[\w.-]+)/search/$',
        desktopdocs.views.search,
        name = 'document-search',
    ),
    url(
        r'^(?P<lang>[a-z-]+)/(?P<version>[\w.-]+)/_images/(?P<path>.*)$',
        desktopdocs.views.images,
    ),
    url(
        r'^(?P<lang>[a-z-]+)/(?P<version>[\w.-]+)/_source/(?P<path>.*)$',
        desktopdocs.views.source,
    ),
    url(
        r'^(?P<lang>[a-z-]+)/(?P<version>[\w.-]+)/(?P<url>[\w./-]*)/$',
        desktopdocs.views.document,
        name = 'document-detail',
    ),
)
