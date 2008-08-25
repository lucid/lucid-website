from django.contrib.syndication.feeds import Feed
from desktopsite.apps.blog.models import Entry
import datetime

class WeblogEntryFeed(Feed):
    title = "Lucid Desktop Project Blog"
    link = "http://www.lucid-desktop.org/blog/"
    description = "Latest news about the Lucid Desktop Project."
    
    title_template = "blog/feeds/title.html"
    description_template = "blog/feeds/description.html"
    
    def items(self):
        return Entry.objects.filter(pub_date__lte=datetime.datetime.now())[:10]

    def item_pubdate(self, item):
        return item.pub_date
    
    def item_description(self, item):
        return item.body
