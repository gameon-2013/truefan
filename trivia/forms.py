__author__ = 'mbacho'
from django import forms
from models import ChoiceCategory
from models import Choice
from models import Question
from models import QuestionLevel
from models import OpenTrivia
from django.contrib.auth.models import User

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

    def setup_queries(self,queries,opentrivia):
        if queries is None:
            raise Exception("queries not specified")
        hsh = opentrivia.trivia_hash
        self.fields['trivia'] = forms.CharField(max_length=40, label='trivia', initial=hsh, required=True)

        for i in queries:
            q_id = i['question'].id
            #self.fields['question_%i' % q_id] = forms.IntegerField(label='question_%i' % q_id,initial=q_id,required=True)
            #self.fields['question_%i' % q_id].widget = forms.HiddenInput()
            self.fields['choices_%i' % q_id] = \
                forms.ModelChoiceField(queryset=i['choice_qry'],
                                       widget=forms.RadioSelect(),
                                       empty_label=None,
                                       label=i['question'].content,
                                       )

#class TriviaFormSet(forms.BaseFormSet):
#    def add_field(self,form,,,
    
