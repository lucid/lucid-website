from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^accounts/profile/$', 'desktopsite.apps.accounts.views.profile'),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/$', 'django.contrib.auth.views.login'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
)