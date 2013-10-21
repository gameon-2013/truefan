from django import forms
from models import *
from django.forms import ModelForm

class KeywordForm(ModelForm):
	class Meta:
		model = Keyword
		fields = ('value',)

	value = forms.CharField()

class SampleForm(forms.Form):
	sample = forms.CharField(widget=forms.Textarea)

class BulkKeywordForm(forms.Form):
        value = forms.CharField(widget=forms.Textarea)

