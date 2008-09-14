from django.db import models
from django.contrib.auth.models import User
from desktopsite.apps.repository import managers
from desktopsite.apps.repository.categories import *
from django.contrib import admin
from desktopsite.apps.repository.middleware import threadlocals

class Package(models.Model):
    sysname = models.SlugField("System Name", unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    url = models.URLField("Homepage")
    maintainer = models.ForeignKey(User)
    category = models.CharField(max_length=100, choices=REPOSITORY_CATEGORIES)
    def get_absolute_url(self):
        return "/repository/packages/%s/" % self.sysname
    def get_versions_desc(self):
        return self.version_set.order_by("-name")
    def user_is_maintainer(self):
        return threadlocals.get_current_user().pk == self.maintainer.pk or threadlocals.get_current_user().is_staff

admin.site.register(Package)

    
class Version(models.Model):
    package = models.ForeignKey(Package)
    name = models.CharField(max_length=100, help_text="""<div class="help">Example: 1.2.16-beta2</div>""", unique=True)
    changelog = models.TextField(help_text="""<div class="help">A list of changes since the last release</div>""")
    package_url = models.URLField(help_text="""<div class="help">This is a direct url to the package.<br />
                                               File sharing sites such as mediafire or rapidshare will not work.<br />
                                               If you cannot host the package yourself,<br />
                                               it is suggested that you use <a href="http://omploader.org/">Omploader</a>.</div>""")
    creation_date = models.DateTimeField(auto_now=True, editable=False)
    checksum = models.CharField(max_length=100, help_text="""<div class="help">The md5sum of the package. See <a href="http://www.openoffice.org/dev_docs/using_md5sums.html">this page</a> for details on how to get this.</div>""")
    verified_safe = models.BooleanField(default=False)
    
    def __str__(self):
        return "%s %s" % (self.package.name, self.name)
    
    def get_absolute_url(self):
        return "/repository/packages/%s/%s/" % (self.package.sysname, self.name)
    def get_rating(self):
        return Rating.objects.score_for_version(self.pk)
    def get_rating_for_user(self):
        try:
            return Rating.objects.get(user=threadlocals.get_current_user(), version=self).score
        except:
            return 0
    def is_new(self):
        import datetime
        three_days_ago = datetime.timedelta(days=-3)
        return (datetime.datetime.now() + three_days_ago) <= self.creation_date
    def is_latest(self):
        return self.package.version_set.order_by("-name")[0].pk == self.pk

admin.site.register(Version)

class Rating(models.Model):
    version=models.ForeignKey(Version)
    user=models.ForeignKey(User)
    date = models.DateTimeField(editable=False, auto_now_add=True)
    score=models.IntegerField(choices=((1, "1"),(2, "2"),(3, "3"),(4, "4"),(5, "5")))
    
    objects = managers.RatingsManager()