from django.conf.urls.defaults import *
from django.contrib.auth.models import User

from views import thread, thread_index, new_thread, category_index, thread_category_index
from views import edit_post, rpc, signout, signin
from views import favorite_index, private_index, profile

from rpc import rpc_post, rpc_lookup, rpc_preview
from feeds import LatestPosts

feeds = {
    'latest': LatestPosts,
    }


urlpatterns = patterns('',
    url(r'^$', thread_index, name="forum-index"),
    url(r'^private/$', private_index, name="forum-private-index"),
    url(r'^profile/$', profile, name="forum-profile"),
    url(r'^signout/$', signout),
    url(r'^signin/$', signin),
    url(r'^newtopic/$', new_thread, name="forum-new-thread"),
    url(r'^categories/$', category_index, name="forum-category-index"),
    url(r'^favorites/$', favorite_index, name="forum-favorite-index"),
    url(r'^edit_post/(?P<original>\d+)/$', edit_post),
    url(r'^threads/$', thread_index),
    url(r'^threads/page(?P<page>\d+)/$', thread_index),
    url(r'^threads/id/(?P<thread_id>\d+)/$', thread),
    url(r'^threads/id/(?P<thread_id>\d+)/page(?P<page>\d+)/$', thread),
    url(r'^threads/category/(?P<cat_id>\d+)/$', thread_category_index),
    url(r'^threads/category/(?P<cat_id>\d+)/page(?P<page>\d+)/$', thread_category_index),

    # RPC
    url(r'^rpc/action/$', rpc),
    url(r'^rpc/postrev/$', rpc_post),
    url(r'^rpc/preview/$', rpc_preview),
    url(r'^rpc/user_lookup/$', rpc_lookup,
            {
                'queryset':User.objects.all(),
                'field':'username',
            }
        ),

    # feeds
    url(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
)
# vim: ai ts=4 sts=4 et sw=4
