from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^accounts/profile/$', 'desktopsite.apps.accounts.views.current_user_profile', name="accounts-current-user-profile"),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name="accounts-login"),
    url(r'^accounts/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', name="accounts-logout"),
    url(r'^user/(?P<username>[\w-]+)/$', 'desktopsite.apps.accounts.views.profile', name="accounts-profile"),
)