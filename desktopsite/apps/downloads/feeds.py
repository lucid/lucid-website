from django.contrib.sites.models import Site
from django.contrib.syndication.feeds import Feed
from desktopsite.apps.downloads.models import *


SITE = Site.objects.get_current()

class LatestDownloads(Feed):
    title = str(SITE) + ' Latest Releases'
    link = "/download/"
    description = "Latest releases of Lucid"

    title_template = "snapboard/feeds/latest_title.html"
    description_template = "snapboard/feeds/latest_description.html"

    def items(self):
        return Release.objects.filter(published__exact=True).order_by('-date')[:20]

    def item_pubdate(self, obj):
        return obj.published


class LatestStable(LatestDownloads):
    title = str(SITE) + ' Latest Stable Releases'
    description = "Latest stable releases of Lucid"

    def items(self):
        return Release.objects.filter(published__exact=True, stable__exact=True).order_by('-date')[:20]

class LatestUnstable(LatestDownloads):
    title = str(SITE) + ' Latest Unstable Releases'
    description = "Latest unstable releases of Lucid"

    def items(self):
        return Release.objects.filter(published__exact=True, stable__exact=False).order_by('-date')[:20]
# vim: ai ts=4 sts=4 et sw=4
