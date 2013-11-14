__author__ = 'mbacho'
from django import forms
from models import ChoiceCategory
from models import Choice
from models import Question
from models import QuestionLevel

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question


class QuestionLevelForm(forms.ModelForm):
    class Meta:
        model = QuestionLevel


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice


class ChoiceCategoryForm(forms.ModelForm):
    class Meta:
        model = ChoiceCategory

