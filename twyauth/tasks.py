# background tasks

import django_rq

from twyauth.models import *

def analyze_profile_tweets(profile):
    profile.analyze_last_tweets()

def analyze_all_profile_tweets():
    profiles = TwitterProfile.objects.all()
    queue = django_rq.get_queue()
    
    for i in profiles:
        queue.enqueue(analyze_profile_tweets, i)
