from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from regex.models import *
from forms import *

def keywords(request):
    if request.method != "POST":
        keywords = Keyword.objects.all()
        keyword_form = KeywordForm()
        return render(request, 'regex/keywords.html', {'keywords':keywords, 'form': keyword_form})
    
    keyword_form = KeywordForm(request.POST)
    if not keyword_form.is_valid():
        keywords = Keyword.objects.all()
        return render(request, 'regex/keywords.html', {'keywords':keywords, 'form': keyword_form})

    keyword_value = keyword_form.cleaned_data['value']
    Keyword.objects.create(value=keyword_value)

    return HttpResponseRedirect(reverse("keywords"))

def test_match(request):
    if request.method != "POST":
        sample_form = SampleForm()
        return render(request, 'regex/match.html', {'form': sample_form})

    sample_form = SampleForm(request.POST)
    if not sample_form.is_valid():
        return render(request, 'regex/match.html', {'form': sample_form})

    sample =  sample_form.cleaned_data['sample']
    results = Keyword.match(sample)

    return render(request, 'regex/match.html', {'results': results})

def bulk_keywords(request):
    if request.method != "POST":
        keywords = Keyword.objects.all()
        bulk_form = BulkKeywordForm()
        return render(request, 'regex/bulk.html', { 'keywords': keywords, 'form': bulk_form })
    
    bulk_form = BulkKeywordForm(request.POST)
    if not bulk_form.is_valid():
        keywords = Keyword.objects.all()
        return render(request, 'regex/bulk.html', { 'keywords': keywords, 'form': bulk_form })
    
    value = bulk_form.cleaned_data['value']
    keywds = [i.strip() for i in value.split(',')]
    for keywd in keywds:
        keyword = Keyword(value=keywd)
        keyword.save()
    
    return HttpResponseRedirect(reverse("bulk_keywords"))

