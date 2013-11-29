import twyauth
import django_rq

from django.contrib.auth import authenticate, login, logout as django_logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from requests.exceptions import ConnectionError

from twython import Twython
from trivia.models import UserPoints
from tasks import analyze_profile_tweets

# If you've got your own Profile setup, see the note in the models file
# about adapting this to your own setup.
from twyauth.models import TwitterProfile

def index(request):
    #sign in after sign in error
    if request.user is not None and request.user.is_authenticated():
        return HttpResponseRedirect(request.build_absolute_uri(reverse("twyauth.views.user_timeline")))
    else:
        return render_to_response('twyauth/index.html', {'login_url': request.build_absolute_uri(twyauth.LOGIN_URL)})


def logout(request, redirect_url=twyauth.LOGOUT_REDIRECT_URL):
    django_logout(request)
    request.session.flush()
    return HttpResponseRedirect(request.build_absolute_uri(redirect_url))


def begin_auth(request):
    """
        The view function that initiates the entire handshake.
    """
    try:
        #no need to login twice
        if request.user is not None and request.user.is_authenticated():
            return HttpResponseRedirect(request.build_absolute_uri(reverse("twyauth.views.user_timeline")))

        # Instantiate Twython
        twitter = Twython(twyauth.TWITTER_KEY, twyauth.TWITTER_SECRET)

        # Request an authorization url to send the user to...
        callback_url = request.build_absolute_uri(reverse('twyauth.views.thanks'))
        auth_props = twitter.get_authentication_tokens(callback_url)

        # redirect user to auth url
        request.session['request_token'] = auth_props
        return HttpResponseRedirect(auth_props['auth_url'])
    except ConnectionError, ce:
        return render_to_response('error.html', { 'error_message' : 'Could not connect to twitter. Check your network connection' })
    except Exception, ex:
        return render_to_response('error.html', { 'error_message' : str(ex)})


def thanks(request):
    """
        A user gets redirected here after hitting Twitter and authorizing your app to use their data.
        This is the view that stores the tokens you want for querying data.
    """
    # Now that we've got the magic tokens back from Twitter, we need to exchange
    # for permanent ones and store them...

    #handle denied access error issue #4
    try:
        if request.GET['denied'] is not None:
            return HttpResponseRedirect(request.build_absolute_uri(reverse('home')))
    except Exception as e:
        pass

    oauth_token = request.session['request_token']['oauth_token']
    oauth_token_secret = request.session['request_token']['oauth_token_secret']
    twitter = Twython(twyauth.TWITTER_KEY, twyauth.TWITTER_SECRET,
                      oauth_token, oauth_token_secret)

    # Retrieve the tokens we want...
    authorized_tokens = twitter.get_authorized_tokens(request.GET['oauth_verifier'])
    request.session['final_token'] = authorized_tokens

    # If they already exist, grab them, login and redirect to a page displaying stuff.
    try:
        user = User.objects.get(username=authorized_tokens['screen_name'])
    except User.DoesNotExist:
        # mock a user creation here; no email, password is just the token, etc.
        user = User.objects.create_user(authorized_tokens['screen_name'], None, authorized_tokens['oauth_token_secret'])
        profile = TwitterProfile()
        profile.user = user
        profile.twitter_userid = authorized_tokens['user_id']
        profile.oauth_token = authorized_tokens['oauth_token']
        profile.oauth_secret = authorized_tokens['oauth_token_secret']
        profile.save()
        
        queue = django_rq.get_queue()
        queue.enqueue_call(func=analyze_profile_tweets, args=(profile,), result_ttl=0)

    user = authenticate(
        username=authorized_tokens['screen_name'],
        password=authorized_tokens['oauth_token_secret']
    )

    if user is not None:
        if user.is_active:
            login(request, user)
            print "A/C active"
            #redirect to a success page
        else:
            #disabled/invalid A/C
            print "A/C not active"
    else:
        phase2_auth(request, authorized_tokens)

    return HttpResponseRedirect(request.build_absolute_uri(twyauth.LOGIN_REDIRECT_URL))

def phase2_auth(request, authorized_tokens):
    user = User.objects.get(username=authorized_tokens['screen_name'])

    if user is not None:
        user.set_password(authorized_tokens['oauth_token_secret'])
        user.save()
        #profile = TwitterProfile.objects.filter(twitter_userid_exact=authorized_tokens['user_id'])
        profile = TwitterProfile.objects.get(twitter_userid=authorized_tokens['user_id'])
        profile.oauth_token = authorized_tokens['oauth_token']
        profile.oauth_secret = authorized_tokens['oauth_token_secret']
        profile.save()
        
        queue = django_rq.get_queue()
        queue.enqueue_call(func=analyze_profile_tweets, args=(profile,), result_ttl=0)

        #authenticate & login
        user = authenticate(
            username=authorized_tokens['screen_name'],
            password=authorized_tokens['oauth_token_secret']
        )

        if user is None and user.is_active:
            login(request, user)



def user_timeline(request):
    """An example view with Twython/OAuth hooks/calls to fetch data about the user in question."""

    if not request.user.is_authenticated():
        login_url = request.build_absolute_uri(reverse('home'))
        return HttpResponseRedirect(login_url)

    user = None
    try:
        user = request.user.twitterprofile
        user.oauth_token = request.session['final_token']['oauth_token']
        user.oauth_secret = request.session['final_token']['oauth_token_secret']
        #user.set_password(request.session['final_token']['oauth_token_secret'])  #TODO Ask Oguya why this is here
        user.save()
    except Exception as ex:
        return render_to_response('error.html', { 'error_message' : str(ex) })


    from twython import TwythonAuthError
    from pprint import pprint
    try:
        if user is None:
            raise Exception("User not validated")
        tweets = []
        user_tweets = user.rugbytweet_set.all()
        for dTweet in user_tweets:
            tweets.append(dTweet.text)
        return render_to_response('twyauth/timeline.html', {'tweets':user_tweets, 'login_url': request.build_absolute_uri(twyauth.LOGOUT_URL),})
    except TwythonAuthError as ex:
        #invalid tokens...get new tokens
        if ex.error_code == 401:
            logout_url = request.build_absolute_uri(reverse("twyauth.views.logout"))
            return HttpResponseRedirect(logout_url)
            #return HttpResponse("something's wrong: <br/> %s" % ex.message)
        else:
            return render_to_response('error.html', {'error_message' : "something's wrong: <br/>%s" % str(ex)})
    except BaseException as bex:
        return render_to_response('error.html', { 'error_message': str(bex)})

def get_tweets(api, tweet_limit=twyauth.TWEET_LIMIT):
    tweets = []
    last_id = None
    req_tweets = api.get_user_timeline()
    while len(req_tweets) > 0 and len(tweets) <= tweet_limit:
        if last_id:
            tweets = tweets + req_tweets[1:]
        else:
            tweets = tweets + req_tweets
        last_id = req_tweets[-1]['id']
        req_tweets = api.get_user_timeline(max_id=last_id)
    return tweets

def stats(request):

    if not request.user.is_authenticated():
        login_url = request.build_absolute_uri(reverse('home'))
        return HttpResponseRedirect(login_url)

    from twyauth.models import Truefan_stats
    stats = Truefan_stats()

    #my aggregate truefanship section
    

    #my tweets section
    tweets = stats.rugby_tweets_stats(request.user.id)
    from pprint import pprint

    #my trivia section
    correct_questions = incorrect_questions = 0
    try_trivia = 'none'
    hide_trivia_chart = 'block'
    try:
        user_points = UserPoints.objects.get(user=request.user)
        correct_questions = user_points.correct_questions
        incorrect_questions = user_points.questions_solved - correct_questions
        if correct_questions <= 0 and user_points.questions_solved <= 0:
            try_trivia = 'block'
            hide_trivia_chart = 'none'
    except Exception, ex:
        pass


    #points earned
    points_earned = stats.tweets_points(request.user.id)

    return render_to_response('twyauth/stats.html',
                              {'rugby_related_tweets': tweets['rugby_related_tweets'],
                               'non_rugby_related_tweets': tweets['non_rugby_related_tweets'],
                               'correct_trivia_questions': correct_questions,
                               'incorrect_trivia_questions': incorrect_questions,
                               'try_trivia' : try_trivia,
                               'hide_trivia_chart': hide_trivia_chart})


