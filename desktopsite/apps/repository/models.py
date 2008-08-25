from django.db import models
from django.contrib.auth.models import User
from desktopsite.apps.repository import managers
from desktopsite.apps.repository.categories import *
from django.contrib import admin

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

admin.site.register(Package)

    
class Version(models.Model):
    package = models.ForeignKey(Package)
    name = models.CharField(max_length=100)
    changelog = models.TextField()
    package_url = models.URLField()
    creation_date = models.DateTimeField(auto_now=True, editable=False)
    checksum = models.CharField(max_length=100, editable=False)
    verified_safe = models.BooleanField(default=False)
    
    def __str__(self):
        return "%s %s" % (self.package.name, self.name)
    
    def get_absolute_url(self):
        return "/repository/packages/%s/%s/" % (self.package.sysname, self.name)
    def get_rating(self):
        return Rating.objects.score_for_version(self.pk)
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