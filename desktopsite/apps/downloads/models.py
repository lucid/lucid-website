from django.db import models
from django.contrib import admin
from desktopsite.settings import DOWNLOADS_ROOT, DOWNLOADS_URL
from django.db.models import signals

class Release(models.Model):
    name=models.CharField(max_length=100, unique=True)
    release_notes=models.TextField()
    change_log=models.TextField()
    date=models.DateTimeField(auto_now=True)
    published=models.BooleanField(default=True)
    stable=models.BooleanField(default=True, help_text="If this is not a production-ready version, uncheck this box.")
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return "/download/%s/" % self.name

class File(models.Model):
    file=models.FilePathField(path=DOWNLOADS_ROOT, recursive=True)
    checksum=models.CharField(max_length=100, editable=False)
    release=models.ForeignKey(Release)
    download_count=models.IntegerField(default=0, editable=False)
    size=models.IntegerField(editable=False)
    name=models.CharField(max_length=50, editable=False)

    def __str__(self):
        return self.file
    def calc_fileinfo(self):
        from django.core.files.storage import default_storage
        from django.core.files.base import ContentFile
        import hashlib
        m = hashlib.md5()
        f = default_storage.open(self.file)
        f.open(mode="r")
        while 1:
            buf = f.read(4096)
            if buf == "":
                break;
            m.update(buf)
        f.close()
        self.checksum = m.hexdigest()
        
        import os
        self.size = os.path.getsize(self.file)

        self.name = os.path.basename(self.file)
    def get_download_url(self):
        return "/download/%s/%s" % (self.release.name, self.name)
    def get_file_url(self):
        return "%s/%s" % (DOWNLOADS_URL, self.file.replace(DOWNLOADS_ROOT, ""))

admin.site.register(File)

def do_file_calc(instance, *args, **kwargs):
    instance.calc_fileinfo()

signals.pre_save.connect(do_file_calc, sender=File)

class FileInline(admin.StackedInline):
    model = File
    extra = 2

class ReleaseAdmin(admin.ModelAdmin):
    inlines=[FileInline]

admin.site.register(Release, ReleaseAdmin)
