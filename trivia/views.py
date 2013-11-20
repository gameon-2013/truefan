__author__ = 'mbacho'
# Create your views here.

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from models import Question
from models import QuestionLevel
from models import Choice
from models import ChoiceCategory
from forms import QuestionLevelForm
from forms import QuestionForm
from forms import ChoiceForm
from forms import ChoiceCategoryForm

from random import shuffle

def play(request, level=None):
    if level is None:
        levels = QuestionLevel.objects.all()
        return render_to_response('trivia/trivia.html', {'levels': levels})

    try:
        selected_level = QuestionLevel.objects.get(name=level)
        queries = list(Question.objects.filter(level=selected_level.id))
        shuffle(queries)
        query_choices = []
        for i in queries:
            choice_cats = list(Choice.objects.filter(category=i.correct_choice.category))
            shuffle(choice_cats)
            obj = { 'question' : i, 'choices': choice_cats }
            query_choices.append(obj)
        return render_to_response('trivia/trivia.html', {'level': level, 'questions': query_choices})
    except Exception, ex:
        return render_to_response('error.html', {'error_message': str(ex)})


def questions(request):
    if request.method == "POST":
        frm = QuestionForm(request.POST)
        if frm.is_valid():
            q = Question(
                content = frm.cleaned_data['content'],
                correct_choice = frm.cleaned_data['correct_choice'],
                level = frm.cleaned_data['level']
            )
            q.save()

#        return HttpResponseRedirect(reverse('questions'))
    queries = Question.objects.all()
    levels = QuestionLevel.objects.all()
    question_frm = QuestionForm()
    level_frm = QuestionLevelForm()
    return render_to_response('trivia/questions.html',
                              {'questions': queries, 'levels': levels, 'question_form': question_frm,
                               'level_form': level_frm})


def choices(request):
    if request.method == "POST":
        frm = ChoiceForm(request.POST)
        if frm.is_valid():
            c = Choice(
                content = frm.cleaned_data['content'],
                category = frm.cleaned_data['category'],
            )
            c.save()
#        return HttpResponseRedirect(reverse('choices'))

    choices = Choice.objects.all()
    categories = ChoiceCategory.objects.all()
    choice_frm = ChoiceForm()
    cat_frm = ChoiceCategoryForm()
    return render_to_response('trivia/choices.html',
                              {'choices': choices, 'categories': categories, 'choice_form': choice_frm,
                               'cat_form': cat_frm})


def question_level_save(request):
    frm = QuestionLevelForm(request.POST)
    if frm.is_valid():
        ql = QuestionLevel(
            name = frm.cleaned_data['name'],
        )
        ql.save()

    return HttpResponseRedirect(reverse('questions'))


def choice_cat_save(request):
    frm = ChoiceCategoryForm(request.POST)
    if frm.is_valid():
        cc = ChoiceCategory(
            name = frm.cleaned_data['name'],
        )
        cc.save()

    return HttpResponseRedirect(reverse('choices'))
