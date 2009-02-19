from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from desktopsite.apps.blog.models import Entry as BlogEntry

def index(request):
    return render_to_response('content/index.html', {}, context_instance=RequestContext(request))

def search(request):
    return render_to_response('content/search.html', {
        "query": request.GET['q'],
    }, context_instance=RequestContext(request))
