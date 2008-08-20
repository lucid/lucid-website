from django.db import models
from django.contrib.auth.models import User

class Package(models.Model):
    sysname = models.SlugField("System Name", unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    url = models.URLField("Homepage")
    maintainer = models.ForeignKey(User)
    type = models.CharField(max_length=100, choices=("Application", "Theme", "Translation"))
    def get_rating(self):
        ratings = self.rating_set.all()
        
            
    
class Version(models.Model):
    package = models.ForeignKey(Package)
    creation_date = models.DateField(auto_now=True, editable=False)
    name = models.CharField(max_length=100)
    checksum = models.CharField(max_length=100, editable=False)
    package_url = models.URLField()
    verified_safe = models.BooleanField()

class Rating(models.Model):
    version=models.ForeignKey(Version)
    rating=models.IntegerField(choices=(1,2,3,4,5))