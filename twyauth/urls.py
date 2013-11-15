from django.conf.urls import patterns, include, url


urlpatterns = patterns('',

    # home
    url(r'^$', "twyauth.views.index", name="home"),

    # authorize app and login
    url(r'^login/?$', "twyauth.views.begin_auth", name="twitter_login"),

    # Logout,
    url(r'^logout/?$', "twyauth.views.logout", name="twitter_logout"),  # Calling logout and what not

    # redirect to after authorizing
    url(r'^thanks/?$', "twyauth.views.thanks", name="twitter_callback"),

    # A sample view of users timeline
    url(r'^user_timeline/?$', "twyauth.views.user_timeline", name="twitter_timeline"),

    # Show  statistics
    url(r'^stats/?$', "twyauth.views.stats", name="stats"),

)
