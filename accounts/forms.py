from django import forms as forms
from django.db import models
from models import *
from django.forms import ModelForm

class RegistrationForm(ModelForm):
	"""docstring for ClassName"""
	class Meta:
	    model = UserProfile
	    fields = ('firstname', 'lastname', 'username', 'email')
	firstname = forms.CharField()
	lastname =forms.CharField()	
	username = forms.CharField()
	email = forms.EmailField()
	password = forms.CharField(widget = forms.PasswordInput)

class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget = forms.PasswordInput)

		
