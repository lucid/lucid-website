from desktopsite.apps.downloads.models import *
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from desktopsite.dojango.util import json_response

def index(request):
    releases = Release.objects.filter(published=True, stable=True).order_by("-date")
    try:
        latest = releases[0]
    except IndexError:
        releases = Release.objects.filter(published=True, stable=False).order_by("-date")
        try:
            latest = releases[0]
        except IndexError:
            latest=None
    other_stable = releases[1:]
    other_unstable = Release.objects.filter(published=True, stable=False).order_by("-date")
    return render_to_response('downloads/index.html', {
        'release': latest,
        'other_stable': other_stable,
        'other_unstable': other_unstable,
    }, context_instance=RequestContext(request))

def version_ping(request):
    stable = Release.objects.filter(published=True, stable=True).order_by("-date")
    unstable = Release.objects.filter(published=True, stable=False).order_by("-date")
    try:
        latest_stable = stable[0].name
    except IndexError:
        latest_stable=None

    try:
        latest_unstable = unstable[0].name
    except IndexError:
        latest_unstable=None
   
    return json_response({
        'stable': latest_stable,
        'unstable': latest_unstable
    })

def release(request, name):
    release = get_object_or_404(Release, name=name, published=True)
    return render_to_response('downloads/release.html', {
        'release': release,
    }, context_instance=RequestContext(request))

def file(request, release_name, file_name):
    release = get_object_or_404(Release, name=release_name, published=True)
    file = get_object_or_404(File, name=file_name, release=release)
    #there's a better way of doing this, but this way is easier...
    #file.download_count = file.download_count+1
    #file.save()
    return HttpResponseRedirect(file.get_file_url())
