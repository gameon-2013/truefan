__author__ = 'mbacho'

from django.conf.urls import patterns, url
from views import landing
from views import questions
from views import choices
from views import new_trivia

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^trivia/$', landing, name="trivia"),
    url(r'^trivia/questions/$', questions, name="questions"),
    url(r'^trivia/choices/$', choices, name="choices"),
    url(r'^trivia/new/$', new_trivia, name="new_trivia"),
)
