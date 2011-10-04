from django.shortcuts import render_to_response
from i2.ideas.models import *
from django.template import RequestContext
from django import forms
from django.http import HttpResponseRedirect
import facebook
from django.conf import settings
from django.contrib.auth import login, authenticate
# from i2.ideas.models import Idea
import json
from django.utils import simplejson
from django.http import HttpResponse

def add(request):
    new_message = Message(text=request.GET.get("mes"))
    new_message.save()
    messages = Message.objects.all()
    return HttpResponse(serializers.serialize('json', messages), mimetype='application/json')

def bb(request):
    return render_to_response("bb.html");

def testthisajax(request):
    response_string="hello"
    if request.method == u'GET':
        print "Got here"
        GET = request.GET
        if GET.has_key(u'myid'):
            print "Got here too"
            idvalue = int(GET[u'myid'])
            #print idvalue
            currentidea = Idea.objects.get(pk=idvalue)
            response_string = currentidea.ideadescription
            #response_string = response_string + str(idvalue)
    return HttpResponse(response_string, mimetype='text/plain')

def ideaview(request):
    dictionary_list = getLoginInfo(request)
    return render_to_response('home.html', {
        "facebook_app_id": settings.FACEBOOK_APP_ID,
        "current_user": dictionary_list["current_user"]},
        context_instance=RequestContext(request)
    )

def ideadetail(request, passedid):
    currentidea = Idea.objects.get(pk=passedid)
    print currentidea.ideaname
    dictionary_list = getLoginInfo(request)
    return render_to_response('idea_detail.html', {
        "facebook_app_id": settings.FACEBOOK_APP_ID,
        "current_user": dictionary_list["current_user"],
        "currentidea": currentidea},
        context_instance=RequestContext(request)
    )

def userdetail(request, passedid):
    currentauthor = User.objects.get(pk=passedid)
    currentprofile = UserProfile.objects.get(user=currentauthor)
    print currentauthor.name
    print currentprofile.fbid
    dictionary_list = getLoginInfo(request)
    listofideas = Idea.objects.filter(author=currentauthor).order_by('-created_at')
    return render_to_response('user_detail.html', {
        "facebook_app_id": settings.FACEBOOK_APP_ID,
        "current_user": dictionary_list["current_user"],
        "currentauthor": currentauthor,
        "listofideas": listofideas,
        "currentprofile": currentprofile},
        context_instance=RequestContext(request)
    )

def index(request):
#    import pdb; pdb.set_trace()
#    print settings.FACEBOOK_APP_ID
    dictionary_list = getLoginInfo(request)
    listofideas = Idea.objects.all().order_by('-created_at')
    
#    for idea in listofideas:
#        print idea.pk
    
#    if dictionary_list["current_user"] != None:
#        print dictionary_list["current_user"].pk

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
    message = ''
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        ideas = Idea.objects.filter(ideaname__icontains=q)
        message = 'You searched for %r' % json.dumps(request.GET['q'])
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

#def display_idea(request, idea):
#    return direct_to_template

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


def ajax_example(request):
    if not request.POST:
        return render_to_response('ajax_example.html', {})
    xhr = request.GET.has_key('xhr')
    response_dict = {}
    name = request.POST.get('name', False)
    total = request.POST.get('total', False)
    response_dict.update({'name': name, 'total': total})
    if total:
        try:
            total = int(total)
        except:
            total = False
    if name and total and int(total) == 10:
        response_dict.update({'success': True })
    else:
        response_dict.update({'errors': {}})
        if not name:
            response_dict['errors'].update({'name': 'This field is required'})
        if not total and total is not False:
            response_dict['errors'].update({'total': 'This field is required'})
        elif int(total) != 10:
            response_dict['errors'].update({'total': 'Incorrect total'})
    if xhr:
        return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')
    return render_to_response('ajax_example.html', response_dict)

#Create your views here.
