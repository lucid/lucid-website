from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.models import User
from django.template import RequestContext

def profile(request):
    return render_to_response('accounts/profile.html', {}, context_instance=RequestContext(request))