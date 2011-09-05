from django.shortcuts import render_to_response
from i2.ideas.models import *
from django.template import RequestContext
from django import forms
from django.http import HttpResponseRedirect
import facebook
from django.conf import settings
from django.contrib.auth import login, authenticate
# from i2.ideas.models import Idea

def ideaview(request):
    dictionary_list = getLoginInfo(request)
    return render_to_response('home.html', {
        "facebook_app_id": settings.FACEBOOK_APP_ID,
        "current_user": dictionary_list["current_user"]},
        context_instance=RequestContext(request)
    )


def index(request):
#    import pdb; pdb.set_trace()
    print settings.FACEBOOK_APP_ID
    dictionary_list = getLoginInfo(request)
    listofideas = Idea.objects.all().order_by('-created_at')

    return render_to_response('home.html', {
        "facebook_app_id": settings.FACEBOOK_APP_ID,
        "current_user": dictionary_list["current_user"], 
        "listofideas": listofideas},
        context_instance=RequestContext(request)
    )

def search_form(request):
    return render_to_response('search_form.html', {'variable': ""})

def search(request):
    ideas = ''
    dictionary_list = getLoginInfo(request)
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        ideas = Idea.objects.filter(ideaname__icontains=q)
        message = 'You searched for %r' % request.GET['q']
    else:
        message = 'Search for something!'
    return render_to_response('home.html', {'variable': message, "facebook_app_id": settings.FACEBOOK_APP_ID, "current_user": dictionary_list["current_user"], 'listofideas': ideas})

def ideasubmit(request):
    dictionary_list = getLoginInfo(request)
    print dictionary_list["current_user"]
    if dictionary_list["current_user"] == None:        
        return HttpResponseRedirect('/')
    message = ''
    if request.method == 'POST':
        form = IdeaForm(request.POST)
        if form.is_valid():
            newidea = form.save(commit=False)
            newidea.author = dictionary_list["current_user"]
            newidea.save()
            return HttpResponseRedirect('/')
        else: 
            form = IdeaForm()
            message = 'Not valid'
    else:
        form = IdeaForm()

    return render_to_response('ideasubmit.html', {
        'form': form, 'message': message, "facebook_app_id": settings.FACEBOOK_APP_ID, "current_user": dictionary_list["current_user"], 
    }, context_instance=RequestContext(request))

def getLoginInfo(request):
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

    parts_dict = {}
    parts_dict["message"] = message
    parts_dict["current_user"] = user
    return parts_dict

#Create your views here.
