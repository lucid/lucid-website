from django.conf.urls.defaults import *
from desktopsite.apps.repository.feeds import *

feeds = {
    'latest': LatestPackages,
    'top-rated': TopRated,
    'featured': Featured,
    'package': PackageFeed,
}

urlpatterns = patterns('',
    url(r'^$', "desktopsite.apps.repository.views.index", name="repository-index"),
    url(r'^letter/(?P<letter>[A-Z])/$', "desktopsite.apps.repository.views.byLetter", name="repository-letter"),
    url(r'^category/(?P<category>.+)/$', "desktopsite.apps.repository.views.byCategory", name="repository-category"),
    url(r'^search/$', "desktopsite.apps.repository.views.search", name="repository-search"),
    url(r'^packages/(?P<sysname>[\w-]+)/$', "desktopsite.apps.repository.views.package", name="repository-package"),
    url(r'^packages/(?P<sysname>[\w-]+)/edit/$', "desktopsite.apps.repository.views.editPackage", name="repository-edit-package"),
    url(r'^packages/(?P<sysname>[\w-]+)/newversion/$', "desktopsite.apps.repository.views.newVersion", name="repository-new-version"),
    url(r'^packages/(?P<sysname>[\w-]+)/delete/$', "desktopsite.apps.repository.views.deletePackage", name="repository-delete-package"),
    url(r'^packages/(?P<sysname>[\w-]+)/(?P<version>[\w\.-]+)/$', "desktopsite.apps.repository.views.version", name="repository-version"),
    url(r'^packages/(?P<sysname>[\w-]+)/(?P<version>[\w\.-]+)/edit/$', "desktopsite.apps.repository.views.editVersion", name="repository-edit-version"),
    url(r'^packages/(?P<sysname>[\w-]+)/(?P<version>[\w\.-]+)/delete/$', "desktopsite.apps.repository.views.deleteVersion", name="repository-delete-version"), 
    
    url(r'^vote/$', "desktopsite.apps.repository.views.saveRating", name="repository-vote"),
    url(r'^newpackage/$', "desktopsite.apps.repository.views.newPackage", name="repository-new-package"),
    url(r'^mypackages/$', "desktopsite.apps.repository.views.userPackages", name="repository-user-packages"),
    # feeds
    url(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
)
