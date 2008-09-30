from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^accounts/profile/$', 'desktopsite.apps.accounts.views.current_user_profile', name="accounts-current-user-profile"),
    url(r'^accounts/profile/edit/$', 'desktopsite.apps.accounts.views.edit_profile', name="accounts-edit-profile"),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name="accounts-login"),
    url(r'^accounts/password_change/$', 'django.contrib.auth.views.password_change'),
    url(r'^accounts/password_change_done/$', 'django.contrib.auth.views.password_change_done'),
    url(r'^accounts/password_reset/$', 'django.contrib.auth.views.password_reset'),
    url(r'^accounts/password_reset_confirm/(?P<token>[\w-]+)/(?P<uidb36>[\w-]+)/$', 'django.contrib.auth.views.password_reset_confirm'),
    url(r'^accounts/password_reset_done/$', 'django.contrib.auth.views.password_reset_done'),
    url(r'^accounts/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', name="accounts-logout"),
    url(r'^user/(?P<username>[\w-]+)/$', 'desktopsite.apps.accounts.views.profile', name="accounts-profile"),
)
