from django.conf.urls.defaults import *
from i2.ideas import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.simple import direct_to_template
from i2.ideas.models import *


# this comment is to make sure github is working.
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

idea_detail_info = {
    "queryset" : Idea.objects.all(),
    "template_name": "idea_detail.html",
}

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'i2.views.home', name='home'),
    # url(r'^i2/', include('i2.foo.urls')),

    #(r'^$', index),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
#    (r'^threadedcomments/', include('threadedcomments.urls')),
)

urlpatterns += patterns('ideas.views',
    (r'^$', 'index'),
    (r'^search_form/$', 'search_form'),
    (r'^search/$', 'search'),
    (r'^ideasubmit/$', 'ideasubmit'),
#    (r'^ideaview/$', 'ideaview'),
    (r'^user/(\d+)/$', 'userdetail'),
    (r'^idea/(\d+)/$', 'ideadetail'),
#    (r'^vote/$', 'vote'),
    (r'^bb$', 'bb'),
    (r'^bb/add$', 'add'),
    (r'^testthisajax/$', 'testthisajax'),
)

urlpatterns += staticfiles_urlpatterns()
