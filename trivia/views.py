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


def landing(request):
    return render_to_response('trivia/base.html')


def play(request, level=None):
    if level is None:
        levels = QuestionLevel.objects.all()
        return render_to_response('trivia/trivia.html', {'levels': levels})

    try:
        selected_level = QuestionLevel.objects.get(name=level)
        queries = Question.objects.filter(level=selected_level.id)
        return render_to_response('trivia/trivia.html', {'level': level, 'questions': queries})
    except Exception, ex:
        return render_to_response('error.html', {'error_message': str(ex)})


def questions(request):
    queries = Question.objects.all()
    levels = QuestionLevel.objects.all()
    question_frm = QuestionForm()
    level_frm = QuestionLevelForm()
    return render_to_response('trivia/questions.html',
                              {'questions': queries, 'levels': levels, 'question_form': question_frm,
                               'level_form': level_frm})


def choices(request):
    choices = Choice.objects.all()
    categories = ChoiceCategory.objects.all()
    choice_frm = ChoiceForm()
    cat_frm = ChoiceCategoryForm()
    return render_to_response('trivia/choices.html',
                              {'choices': choices, 'categories': categories, 'choice_form': choice_frm,
                               'cat_form': cat_frm})


def question_save(request):
    frm = QuestionForm(request.POST)
    if frm.is_valid():
        q = Question(
            content = frm.cleaned_data['content'],
            correct_choice = frm.cleaned_data['correct_choice'],
            level = frm.cleaned_data['level']
        )
        q.save()

    return HttpResponseRedirect(reverse('questions'))


def question_level_save(request):
    frm = QuestionLevelForm(request.POST)
    if frm.is_valid():
        ql = QuestionLevel(
            name = frm.cleaned_data['name'],
        )
        ql.save()

    return HttpResponseRedirect(reverse('questions'))


def choice_save(request):
    frm = ChoiceForm(request.POST)
    if frm.is_valid():
        c = Choice(
            content = frm.cleaned_data['content'],
            category = frm.cleaned_data['category'],
        )
        c.save()

    return HttpResponseRedirect(reverse('choices'))


def choice_cat_save(request):
    frm = ChoiceCategoryForm(request.POST)
    if frm.is_valid():
        cc = ChoiceCategory(
            name = frm.cleaned_data['name'],
        )
        cc.save()

    return HttpResponseRedirect(reverse('choices'))