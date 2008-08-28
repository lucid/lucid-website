from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.models import User
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from desktopsite.apps.snapboard.models import SnapboardProfile

@login_required
def current_user_profile(request):
    return profile(request, request.user.username)

def profile(request, username):
    user = get_object_or_404(User, username=username)
    try:
        forum = SnapboardProfile.objects.get(user=user)
    except SnapboardProfile.DoesNotExist:
        forum = {}
    return render_to_response('accounts/profile.html', {
        'puser': user,
        'forum': forum,
        'is_owner': request.user.username == username,
    }, context_instance=RequestContext(request))