from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from desktopsite.apps.repository.models import *
from desktopsite.apps.repository.forms import *
from desktopsite.apps.repository.categories import REPOSITORY_CATEGORIES
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

def index(request):
    latest = Version.objects.all().order_by("-creation_date")[:8]
    top_rated = Rating.objects.top_rated(8)
    featured = Rating.objects.featured(5)
    return render_to_response('repository/index.html', {
        'categories': REPOSITORY_CATEGORIES,
        'latest': latest, 
        'top_rated': top_rated,
        'featured': featured,
    }, context_instance=RequestContext(request))
    
def byLetter(request, letter):
    results = Package.objects.filter(name__startswith=letter)
    return showResults(request, "Packages starting with \"%s\"" % letter, results)
    
def byCategory(request, category):
    results = Package.objects.filter(category__exact=category)
    return showResults(request, "Packages in \"%s\"" % category, results)

@login_required    
def userPackages(request):
    results = Package.objects.filter(maintainer__exact=request.user)
    return showResults(request, "My Packages", results)
    
    
def search(request):
    if request.GET.has_key("q"):
        query = request.GET["q"]
    else:
        query = ""
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
    version = pak.get_versions_desc()
    if not version:
        version = {}
    else:
        version = version[0]
    return render_to_response('repository/package.html', {
        'package': pak,
        'version': version,
    }, context_instance=RequestContext(request))

def version(request, sysname, version):
    pak = get_object_or_404(Package, sysname=sysname)
    version = get_object_or_404(Version, package=pak, name=version)
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
    try:
        rating, created=Rating.objects.get_or_create(version=version, user=request.user,
                                                 defaults={'score': value})
    except Rating.MultipleObjectsReturned:
        #this happens on occasion, not sure why
        Rating.objects.filter(version=version, user=request.user).delete()
        rating = Rating(version=version, user=request.user)
    if value == "0":
        rating.delete()
    else:
        rating.score=value
        rating.save()
    return HttpResponse("ok", mimetype="text/plain")

@login_required
def newPackage(request):
    if request.method == 'POST':
        form = PackageForm(request.POST, request.FILES)
        if form.is_valid():
            package = form.save(commit=False)
            package.maintainer = request.user
            package.save()
            request.user.message_set.create(message='New Package Created')
            return HttpResponseRedirect(package.get_absolute_url())
    else:
        form = PackageForm()
    return render_to_response("repository/form.html", context_instance=RequestContext(request, {
       'title': "New Package",
       'form': form,
    }))


@login_required
def newVersion(request, sysname):
    package = get_object_or_404(Package, sysname=sysname)
    if not package.user_is_maintainer():
        return HttpResponseRedirect(package.get_absolute_url())
    if request.method == 'POST':
        form = VersionForm(request.POST, request.FILES)
        form._requested_package = package
        is_valid = form.is_valid()

        if is_valid:
            version = form.save() #commit=False ommitted purposefully!
            version.package = package
            version.calc_md5sum()
            request.user.message_set.create(message='New Version Created')
            return HttpResponseRedirect(version.get_absolute_url())

    else:
        form = VersionForm()
    return render_to_response("repository/form.html", context_instance=RequestContext(request, {
       'title': "New Version for %s" % package.name,
       'form': form,
    }))
    
@login_required
def editPackage(request, sysname):
    package = get_object_or_404(Package, sysname=sysname)
    if not package.user_is_maintainer():
        return HttpResponseRedirect(package.get_absolute_url())
    if request.method == 'POST':
        form = PackageForm(request.POST, request.FILES, instance=package)
        if form.is_valid():
            package = form.save(commit=False)
            #package.maintainer = request.user
            package.save()
            request.user.message_set.create(message='Changes Saved')
            return HttpResponseRedirect(package.get_absolute_url())
    else:
        form = PackageForm(instance=package)
    return render_to_response("repository/form.html", context_instance=RequestContext(request, {
       'title': "Editing %s" % package.name,
       'form': form,
    }))
    
@login_required
def editVersion(request, sysname, version):
    package = get_object_or_404(Package, sysname=sysname)
    version = get_object_or_404(Version, name=version, package=package)
    if not package.user_is_maintainer():
        return HttpResponseRedirect(package.get_absolute_url())
    if request.method == 'POST':
        form = EditVersionForm(request.POST, request.FILES, instance=version)
        if form.is_valid():
            version = form.save(commit=False)
            version.package = package
            version.save()
            request.user.message_set.create(message='Changes Saved')
            return HttpResponseRedirect(version.get_absolute_url())
    else:
        form = EditVersionForm(instance=version)
    return render_to_response("repository/form.html", context_instance=RequestContext(request, {
       'title': "Editing %s %s" % (package.name, version.name),
       'form': form,
    }))

@login_required
def deleteVersion(request, sysname, version):
    package = get_object_or_404(Package, sysname=sysname)
    version = get_object_or_404(Version, name=version, package=package)
    if not package.user_is_maintainer():
        return HttpResponseRedirect(package.get_absolute_url())
    return doDeleteView(request, version, package.get_absolute_url())
    
@login_required
def deletePackage(request, sysname):
    package = get_object_or_404(Package, sysname=sysname)
    if not package.user_is_maintainer():
        return HttpResponseRedirect(package.get_absolute_url())
    return doDeleteView(request, package, "/repository/")


def doDeleteView(request, object, finishUrl):
    if request.method == 'POST':
       if request.POST.has_key("Yes"):
           request.user.message_set.create(message='%s Deleted.' % object)
           object.delete()
           return HttpResponseRedirect(finishUrl)
       else:
           return HttpResponseRedirect(object.get_absolute_url())
    else:
        return render_to_response("repository/delete.html", context_instance=RequestContext(request, {
            'object': object,
        }))

