from django.conf.urls.defaults import *
from models import Entry # relative import

info_dict = {
    'queryset': Entry.objects.all(),
    'date_field': 'pub_date',
}

def commentRedirect(request, id):
    from django.http import HttpResponseRedirect
    from django.shortcuts import get_object_or_404
    model = get_object_or_404(Entry, pk=id)
    return HttpResponseRedirect("%s#%s" % (model.get_absolute_url(), request.GET['c']))

urlpatterns = patterns('django.views.generic.date_based',
   url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[\w-]+)/$', 'object_detail', dict(info_dict, slug_field='slug'), name="blog-entry"),
   (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$', 'archive_day', info_dict),
   (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$', 'archive_month', info_dict),
   (r'^(?P<year>\d{4})/$', 'archive_year', info_dict),
   url(r'^/?$', 'archive_index', info_dict, name="blog-index"),
   (r'^commentRedirect/(?P<id>\d+)/$', comment_redirect),
)
