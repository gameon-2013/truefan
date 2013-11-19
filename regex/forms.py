from django import forms
from models import *
from django.forms import ModelForm

class KeywordForm(ModelForm):
	class Meta:
		model = Keyword
		fields = ('value', 'weight')

	value = forms.CharField()
	weight = forms.DecimalField(max_digits=5, decimal_places=4, min_value=0.0, max_value=1.0)

class SampleForm(forms.Form):
	sample = forms.CharField(widget=forms.Textarea)

class BulkKeywordForm(forms.Form):
        value = forms.CharField(widget=forms.Textarea)
        weight = forms.DecimalField(max_digits=5, decimal_places=4, min_value=0.0, max_value=1.0)

class TestDataForm(ModelForm):
    class Meta:
        model = TestData
        fields = ('text', 'positive')
