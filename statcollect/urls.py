from django.conf.urls.defaults import *
from i2.ideas import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'i2.views.home', name='home'),
    # url(r'^i2/', include('i2.foo.urls')),

    #(r'^$', index),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('ideas.views',
    (r'^$', 'index'),
    (r'^search_form/$', 'search_form'),
    (r'^search/$', 'search'),
    (r'^ideasubmit/$', 'ideasubmit'),
)

urlpatterns += staticfiles_urlpatterns()
