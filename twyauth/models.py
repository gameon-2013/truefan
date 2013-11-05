import twyauth

from django.db import models
from django.contrib.auth.models import User
from twython import Twython

from regex.models import Keyword

class TwitterProfile(models.Model):
    """
        An example Profile model that handles storing the oauth_token and
        oauth_secret in relation to a user.
    """
    user = models.OneToOneField(User)
    twitter_userid = models.CharField(max_length=50)
    oauth_token = models.CharField(max_length=200)
    oauth_secret = models.CharField(max_length=200)
    since_id = models.BigIntegerField()
    
    def get_api(self):
        return Twython(twyauth.TWITTER_KEY, twyauth.TWITTER_SECRET,
                      self.oauth_token, self.oauth_secret)
    
    def get_tweets(self, tweet_limit=twyauth.TWEET_LIMIT):
        """ retrieves the latest tweets for a user, if it's their
            first time, retrieves their last 200 tweets """
        api = self.get_api()
        tweets = []
        
        if self.since_id and self.since_id > 0:
            since_id = self.since_id
            req_tweets = api.get_user_timeline(since_id=since_id)
            while len(req_tweets) > 0 and len(tweets) <= tweet_limit:
                tweets = tweets + req_tweets
                ids = [tweet['id'] for tweet in req_tweets]
                since_id = max(ids)
                req_tweets = api.get_user_timeline(since_id=since_id)
        else:
            last_id = None
            req_tweets = api.get_user_timeline()
            while len(req_tweets) > 0 and len(tweets) <= tweet_limit:
                possible_last_id = req_tweets[-1]['id']
                
                if last_id:
                    tweets = tweets + req_tweets[1:]
                    
                    if possible_last_id == last_id:
                        break
                else:
                    tweets = tweets + req_tweets

                last_id = possible_last_id
                req_tweets = api.get_user_timeline(max_id=last_id)
                
        return tweets
    
    def analyze_last_tweets(self, tweet_limit=twyauth.TWEET_LIMIT):
        """ get users last tweets and see if they are rugby tweets """
        
        tweets = self.get_tweets(tweet_limit)
        
        # store the latest id
        ids = [tweet['id'] for tweet in tweets]
        self.since_id = max(ids)
        
        # find rugby tweets
        for tweet in tweets:
            matches = Keyword.match(tweet['text'])
            
            if len(matches) > 0:
                rugby_tweet = RugbyTweet()
                rugby_tweet.text = tweet['text']
                rugby_tweet.tweet_id = tweet['id']
                rugby_tweet.created_at = tweet['created_at']
                rugby_tweet.matches = ",".join(matches)
                rugby_tweet.confidence = len(matches)
                rugby_tweet.profile = self
                
                rugby_tweet.save()

class RugbyTweet(models.Model):
    """ stores tweets that are tagged as containing rugby 
        words """
    text = models.CharField(max_length=200)
    tweet_id = models.BigIntegerField()
    created_at = models.CharField(max_length=100, null=True) # TODO remove null
    matches = models.CharField(max_length=200)
    confidence = models.DecimalField(max_digits=6, decimal_places=4)
    profile = models.ForeignKey('TwitterProfile', null=True) # TODO remove null
    
    def __str__(self):
        return self.text + ": "+self.matches
