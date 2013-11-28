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
    since_id = models.BigIntegerField(null=True)
    total_tweets_pulled = models.PositiveIntegerField(max_length=10, null=True, default=0)
    
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
                
        self.total_tweets_pulled += len(tweets)
        self.save()
        return tweets
    
    def analyze_last_tweets(self, tweet_limit=twyauth.TWEET_LIMIT):
        """ get users last tweets and see if they are rugby tweets """
        
        tweets = self.get_tweets(tweet_limit)
        
        if len(tweets) > 0:
        
            # store the latest id
            ids = [tweet['id'] for tweet in tweets]
            self.since_id = max(ids)
            self.save()
            
            # find rugby tweets
            for tweet in tweets:
                matches, confidence = Keyword.match(tweet['text'])
                
                if len(matches) > 0:
                    rugby_tweet = RugbyTweet()
                    rugby_tweet.text = tweet['text']
                    rugby_tweet.tweetid = tweet['id']
                    rugby_tweet.created_at = tweet['created_at']
                    rugby_tweet.matches = ",".join(matches)
                    rugby_tweet.confidence = confidence
                    rugby_tweet.profile = self
                    
                    rugby_tweet.save()

class RugbyTweet(models.Model):
    """ stores tweets that are tagged as containing rugby 
        words """
    text = models.CharField(max_length=200)
    tweetid = models.BigIntegerField()
    created_at = models.CharField(max_length=100, null=True) # TODO remove null
    matches = models.CharField(max_length=200)
    confidence = models.DecimalField(max_digits=6, decimal_places=4)
    profile = models.ForeignKey('TwitterProfile', null=True) # TODO remove null
    
    def __str__(self):
        return self.text + ": "+self.matches

class Truefan_stats(object):

    def tweets_points(self, profile_id):
        """
            calculate the stats of rugby related & non-related
            tweets
        """
        #import pdb
        #pdb.set_trace()
        all_tweets = RugbyTweet.objects.filter(profile=profile_id)
        tweets_count = len(all_tweets)
        rating_points = self.point_checker(len(all_tweets))

        from decimal import Decimal
        try:
            sum_points = 0
            for i in all_tweets:
                sum_points += i.confidence * Decimal(self.point_checker(sum_points))
        except Exception, e:
            pass

        return sum_points


    def rugby_tweets_stats(self, profile_id):
        """
            ruj tweets/total no of tweets
        """
        rugbyTweet = RugbyTweet.objects.filter(profile_id=profile_id)
        pulled_tweets = TwitterProfile.objects.get(user_id=profile_id)

        rugby_related_tweets = non_rugby_related_tweets = 0
        try:
            rugby_related_tweets = len(rugbyTweet)
            non_rugby_related_tweets = pulled_tweets.total_tweets_pulled - len(rugbyTweet)
        except Exception, e:
            pass

        return {"rugby_related_tweets": rugby_related_tweets,
                "non_rugby_related_tweets": non_rugby_related_tweets}


    def point_checker(self,total_points):
        if total_points >=0 and total_points <= 1001:
            return 10
        elif total_points >= 1001 and total_points <= 2001:
            return 8
        elif total_points > 2001:
            return 6