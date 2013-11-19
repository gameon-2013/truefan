from django.conf.urls import patterns, include, url
from views import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^regex/keywords/$', keywords, name="keywords"),
    url(r'^regex/match/$', test_match, name="match"),
    url(r'^regex/bulk_keywords/$', bulk_keywords, name="bulk_keywords"),
    url(r'^regex/remove/(\d+)/$', remove_keyword, name="remove_keyword"), 
    # Examples:
    # url(r'^$', 'truefan.views.home', name='home'),
    # url(r'^truefan/', include('truefan.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
