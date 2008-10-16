from django.contrib.syndication.feeds import Feed
from desktopsite.apps.blog.models import Entry
import datetime

class WeblogEntryFeed(Feed):
    title = "The Lucid Blog"
    link = "http://www.lucid-desktop.org/blog/"
    description = "Latest news about Lucid Desktop"

    def items(self):
        return Entry.objects.filter(pub_date__lte=datetime.datetime.now())[:10]

    def item_pubdate(self, item):
        return item.pub_date
