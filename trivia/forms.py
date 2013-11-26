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


class TriviaForm(forms.Form):
    def __init__(self, queries, *args, **kwargs):
        super(TriviaForm, self).__init__(*args, **kwargs)
        if queries is None:
            raise Exception("queries not specified")

        for i in queries:
            self.fields['question_%i' % i['question'].id] = forms.CharField()#forms.HiddenInput()
            self.fields['choices_%i' % i['question'].id] = \
                forms.ModelChoiceField(queryset=i['choices'],
                                       widget=forms.RadioSelect,
                                       empty_label=None)
            self.fields['selected_%i' % i['question'].correct_choice.id] = forms.CharField()#forms.HiddenInput()


