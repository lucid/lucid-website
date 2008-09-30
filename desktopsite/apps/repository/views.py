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
    rating, created=Rating.objects.get_or_create(version=version, user=request.user,
                                                 defaults={'score': value})
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
    if package.maintainer.pk != request.user.pk:
        return HttpResponseRedirect(package.get_absolute_url())
    if request.method == 'POST':
        form = VersionForm(request.POST, request.FILES)
        is_valid = form.is_valid()
        version_exists=True
        try:
            Version.objects.get(name=form.cleaned_data["name"], package=package)
        except Version.DoesNotExist:
            version_exists=False
        if is_valid and not version_exists:
            version = form.save(commit=False)
            version.package = package
            version.save()
            version.calc_md5sum()
            request.user.message_set.create(message='New Version Created')
            return HttpResponseRedirect(version.get_absolute_url())
        elif version_exists:
            form.errors["name"] = ["Version with that name already exists"]
    else:
        form = VersionForm()
    return render_to_response("repository/form.html", context_instance=RequestContext(request, {
       'title': "New Version for %s" % package.name,
       'form': form,
    }))
    
@login_required
def editPackage(request, sysname):
    package = get_object_or_404(Package, sysname=sysname)
    if package.maintainer.pk != request.user.pk:
        return HttpResponseRedirect(package.get_absolute_url())
    if request.method == 'POST':
        form = PackageForm(request.POST, request.FILES, instance=package)
        if form.is_valid():
            package = form.save(commit=False)
            package.maintainer = request.user
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
    if package.maintainer.pk != request.user.pk:
        return HttpResponseRedirect(package.get_absolute_url())
    if request.method == 'POST':
        form = VersionForm(request.POST, request.FILES, instance=version)
        if form.is_valid():
            version = form.save(commit=False)
            version.package = package
            version.save()
            request.user.message_set.create(message='Changes Saved')
            return HttpResponseRedirect(version.get_absolute_url())
    else:
        form = VersionForm(instance=version)
    return render_to_response("repository/form.html", context_instance=RequestContext(request, {
       'title': "Editing %s %s" % (package.name, version.name),
       'form': form,
    }))
