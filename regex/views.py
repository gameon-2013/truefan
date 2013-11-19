from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from regex.models import *
from forms import *

def keywords(request):
    keyword_form = KeywordForm(request.POST or None)
    if not keyword_form.is_valid():
        keywords = Keyword.objects.all()
        return render(request, 'regex/keywords.html', {'keywords':keywords, 'form': keyword_form})

    keyword_value = keyword_form.cleaned_data['value']
    keyword_weight = keyword_form.cleaned_data['weight']
    Keyword.objects.create(value=keyword_value, weight=keyword_weight)

    return HttpResponseRedirect(reverse("keywords"))

def test_match(request):
    sample_form = SampleForm(request.POST or None)
    if not sample_form.is_valid():
        return render(request, 'regex/match.html', {'form': sample_form})

    sample =  sample_form.cleaned_data['sample']
    results = Keyword.match(sample)

    return render(request, 'regex/match.html', {'results': results})

def bulk_keywords(request):
    bulk_form = BulkKeywordForm(request.POST or None)
    if not bulk_form.is_valid():
        keywords = Keyword.objects.all()
        return render(request, 'regex/bulk.html', { 'keywords': keywords, 'form': bulk_form })
    
    value = bulk_form.cleaned_data['value']
    weight = bulk_form.cleaned_data['weight']
    keywds = [i.strip() for i in value.split(',')]
    for keywd in keywds:
        keyword = Keyword(value=keywd, weight=weight)
        keyword.save()
    
    return HttpResponseRedirect(reverse("bulk_keywords"))

def remove_keyword(request, keyword):
    keyword = get_object_or_404(Keyword, pk=keyword)
    keyword.delete()
    
    return HttpResponseRedirect(reverse("bulk_keywords"))
    
