from django.conf.urls.defaults import *
from models import Entry # relative import

info_dict = {
    'queryset': Entry.objects.all(),
    'date_field': 'pub_date',
}

urlpatterns = patterns('django.views.generic.date_based',
   url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[\w-]+)/$', 'object_detail', dict(info_dict, slug_field='slug'), name="blog-entry"),
   url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$', 'archive_day', info_dict, name="blog-day-archive"),
   url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$', 'archive_month', info_dict, name="blog-month-archive"),
   url(r'^(?P<year>\d{4})/$', 'archive_year', info_dict, name="blog-year-archive"),
   url(r'^/?$', 'archive_index', info_dict, name="blog-index"),
)
