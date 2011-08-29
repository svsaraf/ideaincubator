from django.shortcuts import render_to_response
from i2.ideas.models import *
from django.template import RequestContext
from django import forms
from django.http import HttpResponseRedirect
import facebook
from django.conf import settings
from django.contrib.auth import login, authenticate

def index(request):
#    import pdb; pdb.set_trace()
    print settings.FACEBOOK_APP_ID
    cookie = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_APP_ID, settings.FACEBOOK_APP_SECRET)
    message = ''
    user = None
    if cookie:
        print cookie
        try:
            up = UserProfile.objects.get(fbid=cookie['uid'])
            print up.access_token
            user = up.user
        except UserProfile.DoesNotExist:
            graph = facebook.GraphAPI(cookie["access_token"])
            profile = graph.get_object("me")
            print profile

            try:
                genUser = profile['first_name'] + profile['id']
                user = User.objects.get(username=genUser)
            except User.DoesNotExist:
                user = User.objects.create_user(username=genUser, email='test@example.com', password=genUser)
                user.first_name = profile['first_name']
                user.last_name = profile['last_name']
                user.save()

            up = UserProfile(user=user, fbid=cookie['uid'], access_token=cookie['access_token'])
            up.save()
        user = authenticate(username=user.username, password=user.username)
        if user is not None:
            login(request, user)
        else:
            print "user was none"
    else:
        message='Log in'

    return render_to_response('index.html', {
        'variable': "here",
        "facebook_app_id": settings.FACEBOOK_APP_ID,
        "message": message,
        "current_user": user}, 
        context_instance=RequestContext(request)
    )

def search_form(request):
    return render_to_response('search_form.html', {'variable': ""})

def search(request):
    ideas = ''
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        ideas = Idea.objects.filter(ideaname__icontains=q)
        message = 'You searched for %r' % request.GET['q']
    else:
        message = 'Search for something!'
    return render_to_response('search_form.html', {'variable': message, 'ideas': ideas})

def ideasubmit(request):
    message = ''
    if request.method == 'POST':
        form = IdeaForm(request.POST)
        if form.is_valid():
            newidea = form.save(commit=False)
            newidea.save()
            return HttpResponseRedirect('/search_form/')
        else: 
            form = IdeaForm()
            message = 'Not valid'
    else:
        form = IdeaForm()

    return render_to_response('ideasubmit.html', {
        'form': form, 'message': message,
    }, context_instance=RequestContext(request))


#Create your views here.
