from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from desktopsite.apps.repository.models import *
from desktopsite.apps.repository.categories import REPOSITORY_CATEGORIES
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

def index(request):
    latest = Version.objects.all().order_by("creation_date")[:8]
    top_rated = Rating.objects.top_rated(8)
    return render_to_response('repository/index.html', {
        'categories': REPOSITORY_CATEGORIES,
        'latest': latest, 
        'top_rated': top_rated                                                  
    }, context_instance=RequestContext(request))
    
def byLetter(request, letter):
    results = Package.objects.filter(name__startswith=letter)
    return showResults(request, "Packages starting with \"%s\"" % letter, results)
    
def byCategory(request, category):
    results = Package.objects.filter(category__exact=category)
    return showResults(request, "Packages in \"%s\"" % category, results)
    
def search(request):
    query = request.GET["q"]
    if query:
        results = Package.objects.filter(name__contains=query)
    else:
        results = []
    return showResults(request, "Results for \"%s\"" % query, results)
    
def showResults(request, title, resultset):
    return render_to_response('repository/results.html', {
        'results': resultset,
        'title': (title if title else "Search Results"),
    }, context_instance=RequestContext(request))
    
def package(request, sysname):
    pak = get_object_or_404(Package, sysname=sysname)
    return render_to_response('repository/package.html', {
        'package': pak,
        'version': pak.get_versions_desc()[0],
    }, context_instance=RequestContext(request))

def version(request, sysname, version):
    pak = get_object_or_404(Package, sysname=sysname)
    version = get_object_or_404(pak.version_set, name=version)
    return render_to_response('repository/version.html', {
        'package': pak,
        'version': version,
    }, context_instance=RequestContext(request))
    
@login_required
def saveRating(request):
    pk = request.POST["versionId"]
    version = get_object_or_404(Version, pk=pk)
    value = request.POST["value"]
    if not (value < 0 or value > 5):
        return HttpResponse("nice try asshole", mimetype="text/plain")
    rating, created=Rating.objects.get_or_create(version=version, user=request.user,
                                                 defaults={'score': value})
    if value == "0":
        rating.delete()
    else:
        rating.score=value
        rating.save()
    return HttpResponse("ok", mimetype="text/plain")