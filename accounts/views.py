from forms import *
from models import *
from django.contrib import auth
from django.contrib.auth.models import User
from django import forms as forms
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def index(request):
	return render_to_response('index.html')

def registration(request):	
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			email = form.cleaned_data['email']
			firstname = form.cleaned_data['firstname']
			lastname = form.cleaned_data['lastname']

			usernamecheck = User.objects.filter(username = username)#check if username exists
			if usernamecheck:
				error = "Username already in use choose another one."
				return render_to_response('registration.html', {'error' : error, 'form' : form}, context_instance = RequestContext(request))

			#create user object then save it
			user = User.objects.create_user(username = username, password = password, email = email, firstname=firstname, lastname = lastname)
			user = user.save()
			user = User.objects.get(username = username)

			#create user profile then save it
			new_userprofile = form.save(commit = False)
			new_userprofile.user = user
			new_userprofile.save()

			#authenticate user then start session
			authenticated_user = auth.authenticate(username = username, password = password)
			if authenticated_user:
				auth.login(request, authenticated_user)
				request.session['username'] = username
				return HttpResponseRedirect("home")			
	else:
		form = RegistrationForm()
		return render_to_response('registration.html', {'form' : form}, context_instance = RequestContext(request))

def home(request):
	print request.session['username']
	return render_to_response('home.html', context_instance = RequestContext(request))

def login(request):
	form = LoginForm()
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			authenticated_user = auth.authenticate(username = username, password = password)
			if authenticated_user:
				auth.login(request, authenticated_user)
				request.session['username'] = username
				return  HttpResponseRedirect('home', )
			else:
				error = "Username and password do not match"
				return render_to_response('login.html', {'error': error, 'form' : form}, context_instance = RequestContext(request))
	return render_to_response('login.html', {'form' : form}, context_instance = RequestContext(request))

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect("/")





# Create your views here.

