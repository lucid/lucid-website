from django.db import models
from django.contrib.auth.models import User
from desktopsite.apps.repository import managers

class Package(models.Model):
    sysname = models.SlugField("System Name", unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    url = models.URLField("Homepage")
    maintainer = models.ForeignKey(User)
    type = models.CharField(max_length=100, choices=(
                                                     ("application", "Application"),
                                                     ("theme", "Theme"),
                                                     ("translation", "Translation"),
                                                    ))
    def get_absolute_url(self):
        return "#"
            
    
class Version(models.Model):
    package = models.ForeignKey(Package)
    creation_date = models.DateField(auto_now=True, editable=False)
    name = models.CharField(max_length=100)
    checksum = models.CharField(max_length=100, editable=False)
    package_url = models.URLField()
    verified_safe = models.BooleanField()
    
    def __str__(self):
        return "%s %s" % (self.package.name, self.name)
    
    def get_absolute_url(self):
        return "#"
    def get_rating(self):
        return Rating.objects.score_for_version(self.pk)

class Rating(models.Model):
    version=models.ForeignKey(Version)
    user=models.ForeignKey(User)
    date = models.DateTimeField(editable=False, auto_now_add=True)
    score=models.IntegerField(choices=((1, "1"),(2, "2"),(3, "3"),(4, "4"),(5, "5")))
    
    objects = managers.RatingsManager()