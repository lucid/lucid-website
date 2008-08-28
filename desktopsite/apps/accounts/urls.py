from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^accounts/profile/$', 'desktopsite.apps.accounts.views.current_user_profile'),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/$', 'django.contrib.auth.views.login'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    (r'^user/(?P<username>[\w-]+)/$', 'desktopsite.apps.accounts.views.profile'),
)