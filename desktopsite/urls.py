from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^forum/', include('desktopsite.apps.snapboard.urls')),
    (r'^blog/', include('desktopsite.apps.blog.urls')),
    (r'^admin/', include('django.contrib.admin.urls')),
    (r'^dojango/', include('dojango.urls')),
    (r'', include('desktopsite.apps.content.urls')),
    (r'', include('django.contrib.flatpages.urls')),
)
