from django.contrib.auth import authenticate, login, logout as django_logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse

import twyauth

from twython import Twython

# If you've got your own Profile setup, see the note in the models file
# about adapting this to your own setup.
from twyauth.models import TwitterProfile

def index(request):
    return render_to_response('twyauth/index.html')


def logout(request, redirect_url=twyauth.LOGOUT_REDIRECT_URL):
    django_logout(request)
    return HttpResponseRedirect(request.build_absolute_uri(redirect_url))


def begin_auth(request):
    """
        The view function that initiates the entire handshake.
    """
    # Instantiate Twython
    twitter = Twython(twyauth.TWITTER_KEY, twyauth.TWITTER_SECRET)

    # Request an authorization url to send the user to...
    callback_url = request.build_absolute_uri(reverse('twyauth.views.thanks'))
    auth_props = twitter.get_authentication_tokens(callback_url)

    # redirect user to auth url
    request.session['request_token'] = auth_props
    return HttpResponseRedirect(auth_props['auth_url'])


def thanks(request):
    """
        A user gets redirected here after hitting Twitter and authorizing your app to use their data.
        This is the view that stores the tokens you want for querying data.
    """
    # Now that we've got the magic tokens back from Twitter, we need to exchange
    # for permanent ones and store them...
    oauth_token = request.session['request_token']['oauth_token']
    oauth_token_secret = request.session['request_token']['oauth_token_secret']
    twitter = Twython(twyauth.TWITTER_KEY, twyauth.TWITTER_SECRET,
                      oauth_token, oauth_token_secret)

    # Retrieve the tokens we want...
    authorized_tokens = twitter.get_authorized_tokens(request.GET['oauth_verifier'])

    # If they already exist, grab them, login and redirect to a page displaying stuff.
    try:
        user = User.objects.get(username=authorized_tokens['screen_name'])
    except User.DoesNotExist:
        # mock a user creation here; no email, password is just the token, etc.
        user = User.objects.create_user(authorized_tokens['screen_name'], "<<email here>>", authorized_tokens['oauth_token_secret'])
        profile = TwitterProfile()
        profile.user = user
        profile.oauth_token = authorized_tokens['oauth_token']
        profile.oauth_secret = authorized_tokens['oauth_token_secret']
        profile.save()

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
        return HttpResponse("invalid login msg")
        #invalid login msg

    return HttpResponseRedirect(twyauth.LOGIN_REDIRECT_URL)


def user_timeline(request):
    """An example view with Twython/OAuth hooks/calls to fetch data about the user in question."""
    import json
    user = request.user.twitterprofile
    tweets = []
    twitter = Twython(twyauth.TWITTER_KEY, twyauth.TWITTER_SECRET,
                      user.oauth_token, user.oauth_secret)
    user_tweets = twitter.get_user_timeline()
    for dTweet in user_tweets:
        tweets.append(dTweet['text'])
    return render_to_response('twyauth/timeline.html', {'tweets':tweets, 'login_url': twyauth.LOGOUT_URL,})