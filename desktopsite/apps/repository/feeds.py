from django.contrib.sites.models import Site
from django.contrib.syndication.feeds import Feed
from desktopsite.apps.repository.models import *
from django.core.exceptions import ObjectDoesNotExist

SITE = Site.objects.get_current()

class LatestPackages(Feed):
    title = str(SITE) + ' Latest Packages'
    link = "/repository/"
    description = "The latest community packages for Lucid"

    title_template = "repository/feeds/title.html"
    description_template = "repository/feeds/description.html"

    def items(self):
        return Version.objects.all().order_by("-creation_date")[:20]

    def item_pubdate(self, obj):
        return obj.creation_date

    def item_categories(self, obj):
        return [obj.package.category]

    def item_author_name(self, obj):
        return obj.package.maintainer.username

    def item_author_email(self, obj):
        return 'http://' + SITE.domain + obj.package.maintainer.get_absolute_url()

class TopRated(LatestPackages):
    title = str(SITE) + ' Top Rated Packages'
    description = "Top rated community packages for Lucid"

    def items(self):
        return Rating.objects.top_rated(20)

class Featured(LatestPackages):
    title = str(SITE) + ' Featured Packages'
    description = "Featured community packages for Lucid"

    def items(self):
        return Rating.objects.featured(20)

class PackageFeed(LatestPackages):
    description_template = "repository/feeds/description_package.html"

    def title(self, obj):
        return str(SITE) + " Package Repository - %s" % obj.name

    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return obj.get_absolute_url()

    def description(self, obj):
        return "Latest releases of %s" % obj.name

    def get_object(self, bits):
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return Package.objects.get(sysname=bits[0])
    
    def items(self, obj):
        return obj.get_versions_desc()[:20]

        
# vim: ai ts=4 sts=4 et sw=4
