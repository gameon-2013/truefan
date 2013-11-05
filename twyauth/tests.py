import twython

from django.test import TestCase
from mock import patch, Mock

from regex.models import Keyword
from models import *

tweets = [
    {
        'id': 12500,
        'text': 'its been awhile by Staind',
        'created_at': None,
    },
    {
        'id': 12470,
        'text': 'safari sevens here we come',
        'created_at': None,
    },
    {
        'id': 12420,
        'text': 'this is rugby nation',
        'created_at': None,
    },
    {
        'id': 12400,
        'text': 'later',
        'created_at': None,
    },
    {
        'id': 12345,
        'text': 'hello world',
        'created_at': None,
    },
    
]

def custom_timeline(*args, **kargs):
    if 'since_id' in kargs:
        since_tweets = [tweet for tweet in tweets if tweet['id'] > kargs['since_id']]
        return since_tweets
    
    if 'max_id' in kargs:
        max_tweets = [tweet for tweet in tweets if tweet['id'] <= kargs['max_id']]
        return max_tweets
    
    return tweets

class TwitterProfileTest(TestCase):
    """ tests for TwitterProfile model """
    
    def setUp(self):
        self.patcher2 = patch('twython.Twython')
        Twython_Mock = self.patcher2.start()
        Twython_Mock.return_value.get_user_timeline.side_effect = custom_timeline
        
        self.patcher = patch.object(TwitterProfile, 'get_api', lambda obj: Twython_Mock())
        
        self.patcher.start()
        
        self.profile = TwitterProfile()    
    
    def tearDown(self):
        self.patcher.stop()
        self.patcher2.stop()
    
    def test_get_old_tweets(self):
        """ test results gotten without since_id """
        tweets = self.profile.get_tweets()
        self.assertEqual(5, len(tweets), "Actual Tweet Results: %s" % repr(tweets))
    
    def test_get_latest_tweets(self):
        """ test results gotten with since_id """
        self.profile.since_id = 12420
        tweets = self.profile.get_tweets()
        self.assertEqual(2, len(tweets), "Actual Tweet Results: %s" % repr(tweets))
    
    def test_analyze_tweets(self):
        """ tests for rugby tweets """
        keywords = ['rugby', 'safari', 'sevens']
        for k in keywords:
            Keyword.objects.create(value=k)
        
        self.profile.analyze_last_tweets()
        rugby_tweets = RugbyTweet.objects.all()
        self.assertEqual(2, len(rugby_tweets), "Actual Rugby Tweets: %s" % repr(rugby_tweets))
        self.assertEqual(12500, self.profile.since_id, "Actual Since ID: %i" % self.profile.since_id)

