from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'', include('twyauth.urls')),
    url(r'', include('regex.urls')),
    url(r'', include('trivia.urls')),
    url(r'^django-rq/', include('django_rq.urls')),
    #url(r'', include('stats.urls')),
    # Examples:
    # url(r'^$', 'truefan.views.home', name='home'),
    # url(r'^truefan/', include('truefan.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
