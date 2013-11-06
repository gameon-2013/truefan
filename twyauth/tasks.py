# background tasks

from twyauth.models import *

def analyze_profile_tweets(profile):
    profile.analyze_last_tweets()

def analyze_all_profile_tweets():
    profiles = TwitterProfile.objects.all()
    for i in profiles:
        i.analyze_last_tweets()
