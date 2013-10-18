from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from regex.models import Keyword, CompiledRegex
from forms import *

def keywords(request):
    if request.method != "POST":
        keywords = Keyword.objects.all()
        latest = CompiledRegex.latest()
        keyword_form = KeywordForm()
        return render(request, 'regex/keywords.html', {'keywords':keywords, 'latest':latest, 'form': keyword_form})
    
    keyword_form = KeywordForm(request.POST)
    if not keyword_form.is_valid():
        keywords = Keyword.objects.all()
        latest = CompiledRegex.latest()
        return render(request, 'regex/keywords.html', {'keywords':keywords, 'latest':latest, 'form': keyword_form})

    keyword_value = keyword_form.cleaned_data['value']
    keyword = Keyword(value=keyword_value)
    keyword.save()

    return HttpResponseRedirect(reverse("keywords"))

def test_match(request):
    if request.method != "POST":
        sample_form = SampleForm()
        return render(request, 'regex/match.html', {'form': sample_form})

    sample_form = SampleForm(request.POST)
    if not sample_form.is_valid():
        return render(request, 'regex/match.html', {'form': sample_form})

    sample =  sample_form.cleaned_data['sample']
    results = CompiledRegex.match(sample)

    return render(request, 'regex/match.html', {'results': results})