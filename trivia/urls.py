__author__ = 'mbacho'

from django.conf.urls import patterns, url
from views import landing
from views import questions
from views import choices
from views import play
from views import question_level_save
from views import choice_cat_save
from views import  choice_save
from views import question_save


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^trivia/$', landing, name="trivia"),
    url(r'^trivia/questions/$', questions, name="questions"),
    url(r'^trivia/choices/$', choices, name="choices"),
    url(r'^trivia/play/$', play, name="play"),
    url(r'^trivia/play/([A-Z a-z]+)/$', play, name="play"),
    url(r'^trivia/quest_save/$', question_save, name="question_save"),
    url(r'^trivia/quest_lvl_save/$', question_level_save, name="question_level_save"),
    url(r'^trivia/choice_save/$', choice_save, name="choice_save"),
    url(r'^trivia/choice_cat_save/$', choice_cat_save, name="choice_cat_save"),
)
