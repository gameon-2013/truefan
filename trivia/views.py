__author__ = 'mbacho'
# Create your views here.

from random import shuffle

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from models import Question
from models import QuestionLevel
from models import Choice
from models import ChoiceCategory
from models import UserPoints
from forms import QuestionLevelForm
from forms import QuestionForm
from forms import ChoiceForm
from forms import ChoiceCategoryForm
from forms import TriviaForm


def get_queries(form):
    data = form.data
    query_ids = [i[i.index('_') + 1:] for i in data.keys()]
    val_ids = [int(i) for i in data.values()]
    queries = []
    l = len(form.data)
    for i in range(0, l, 1):
        q = Question.objects.get(id=int(query_ids[i]))
        obj = {'question': q, 'correct': q.correct_choice_id == val_ids[i]}
        if obj['correct']:
            obj['selected'] = q.correct_choice
        else:
            obj['selected'] = Choice.objects.get(id=int(val_ids[i]))
        queries.append(obj)
    return queries


def score(request, level):
    #TODO remove error allowing user to save multiple times using browser refresh
    if request.method != "POST":
        return HttpResponseRedirect('play')

    frm = TriviaForm(request.POST or None)
    if not frm.is_valid():
        return render_to_response('trivia/trivia.html', {'trivia_frm': frm,'user':request.user})

    queries = get_queries(frm)
    total_correct = reduce(lambda x, y: x + (1 if y['correct'] else 0), queries, 0)
    lvl = QuestionLevel.objects.get(name=level)
    total_score = lvl.points * total_correct
    total_questions = len(queries)

    user = request.user
    if user.is_authenticated():
        userscore = None
        try:
            userscore = UserPoints.objects.get(user=user)
        except:
            userscore = UserPoints(user=user)
        userscore.points += total_score
        userscore.correct_questions += total_correct
        userscore.questions_solved += total_questions
        userscore.save()
    return render_to_response('trivia/score.html', {
        'correct': total_correct, 'total': total_questions,
        'score': total_score, 'queries': queries, 'level': lvl,
        'active_tab': 'play','perc':(total_correct/total_questions),'user':user
    })


def play(request, level=None):
    if level is None:
        levels = QuestionLevel.objects.all()
        return render_to_response('trivia/trivia.html', {'levels': levels,'user':request.user, 'active_tab': 'play'})

    selected_level = QuestionLevel.objects.get(name=level)
    queries = list(Question.objects.filter(level=selected_level.id))
    shuffle(queries)
    query_choices = []

    try:
        for i in queries:
            choice_qry = Choice.objects.filter(category=i.correct_choice.category).exclude(id=i.correct_choice_id)[:3]
            choice_cats = list(choice_qry)
            choice_cats.append(i.correct_choice)
            shuffle(choice_cats)
            obj = {'question': i, 'choices': choice_cats, 'choice_qry': choice_qry, 'selected': None}
            query_choices.append(obj)

        frm = TriviaForm()
        frm.setup_queries(query_choices)
        return render_to_response('trivia/trivia.html',
                                  {'level': level, 'questions': query_choices,'len':len(query_choices),
                                   'user':request.user, 'active_tab': 'play', 'trivia_form': frm})
    except Exception, ex:
        return render_to_response('error.html', {'error_message': str(ex)})


# @login_required(login_url='/')
def questions(request):
    frm = QuestionForm(request.POST or None)

    if frm.is_valid():
        q = Question(
            content=frm.cleaned_data['content'],
            correct_choice=frm.cleaned_data['correct_choice'],
            level=frm.cleaned_data['level']
        )
        q.save()

    #   return HttpResponseRedirect(reverse('questions'))
    queries = Question.objects.all()
    levels = QuestionLevel.objects.all()
    question_frm = QuestionForm()
    level_frm = QuestionLevelForm()
    return render_to_response('trivia/questions.html',
                              {'questions': queries, 'levels': levels, 'question_form': question_frm,
                               'level_form': level_frm, 'user': request.user, 'active_tab': 'questions'})


# @login_required(login_url='/')
def choices(request):
    frm = ChoiceForm(request.POST or None)
    if frm.is_valid():
        c = Choice(
            content=frm.cleaned_data['content'],
            category=frm.cleaned_data['category'],
        )
        c.save()
        #   return HttpResponseRedirect(reverse('choices'))

    choices = Choice.objects.all()
    categories = ChoiceCategory.objects.all()
    choice_frm = ChoiceForm()
    cat_frm = ChoiceCategoryForm()
    return render_to_response('trivia/choices.html',
                              {'choices': choices, 'categories': categories, 'choice_form': choice_frm,
                               'user':request.user, 'cat_form': cat_frm, 'active_tab': 'choices'})


# @login_required(login_url='/')
def question_level_save(request):
    frm = QuestionLevelForm(request.POST or None)
    if frm.is_valid():
        ql = QuestionLevel(
            name=frm.cleaned_data['name'],
        )
        ql.save()

    return HttpResponseRedirect(reverse('questions'))


# @login_required(login_url='/')
def choice_cat_save(request):
    frm = ChoiceCategoryForm(request.POST or None)
    if frm.is_valid():
        cc = ChoiceCategory(
            name=frm.cleaned_data['name'],
        )
        cc.save()

    return HttpResponseRedirect(reverse('choices'))
