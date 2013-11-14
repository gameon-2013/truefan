__author__ = 'mbacho'
# Create your views here.

from django.shortcuts import render_to_response
from models import Question
from models import QuestionLevel
from models import Choice
from models import ChoiceCategory


def landing(request):
    quest_url = ''
    choice_url = ''
    new_url = ''
    return render_to_response('trivia/landing.html',
                              {'choice_url': choice_url, 'quest_url': quest_url, 'new_url': new_url})

def new_trivia(request):
    return render_to_response('trivia/trivia.html')


def questions(request):
    queries = Question.objects.all()
    levels = QuestionLevel.objects.all()
    return render_to_response('trivia/questions.html', {'questions': queries, 'levels': levels})


def choices(request):
    choices = Choice.objects.all()
    categories = ChoiceCategory.objects.all()
    return render_to_response('trivia/choices.html', {'choices': choices, 'categories': categories})