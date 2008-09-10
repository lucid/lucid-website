import datetime
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

class Entry(models.Model):
    pub_date = models.DateTimeField()
    slug = models.SlugField(unique_for_date='pub_date')
    headline = models.CharField(max_length=200)
    summary = models.TextField(help_text="Use raw HTML.")
    body = models.TextField(help_text="Use raw HTML.")
    author = models.ForeignKey(User, limit_choices_to = {'is_staff__exact': True})

    class Meta:
        db_table = 'blog_entries'
        verbose_name_plural = 'entries'
        ordering = ('-pub_date',)
        get_latest_by = 'pub_date'

    class Admin(admin.ModelAdmin):
        list_display = ('pub_date', 'headline', 'author')

    def __unicode__(self):
        return self.headline

    def get_absolute_url(self):
        return "/blog/%s/%s/" % (self.pub_date.strftime("%Y/%b/%d").lower(), self.slug)
    
    def get_comment_url(self):
        return "/blog/%s/" % self.pk

admin.site.register(Entry, Entry.Admin)