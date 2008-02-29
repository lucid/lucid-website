from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    # (r'^desktopsite/', include('desktopsite.foo.urls')),
    (r'^forum/', include('desktopsite.apps.forum.urls')),
    (r'^blog/', include('desktopsite.apps.blogmaker.blog.urls')),
    (r'^admin/', include('django.contrib.admin.urls')),
)
