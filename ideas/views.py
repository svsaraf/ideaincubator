from django.shortcuts import render_to_response
from i2.ideas.models import *

def index(request):
    return render_to_response('index.html', {'variable': "here"})

def search_form(request):
    return render_to_response('search_form.html', {'variable': ""})

def search(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        ideas = Idea.objects.filter(ideaname__icontains=q)
        message = 'You searched for %r' % request.GET['q']
    else:
        message = 'You submitted an empty form.'
    return render_to_response('search_form.html', {'variable': message, 'ideas': ideas})

#def submitidea(request):
#    if request.method == 'POST':
#        form = IdeaForm(request.POST)
#        if form.isvalid():
#            newidea = form.save(commit=False)
#            newidea.author = 'anonymous'
#            newidea.save()
#    else:
#        form      
#Create your views here.
