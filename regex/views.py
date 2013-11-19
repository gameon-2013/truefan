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

def test_data(request):
    td_form = TestDataForm(request.POST or None)
    if not td_form.is_valid():
        test_datas = TestData.objects.all()
        return render(request, 'regex/test_data.html', {'form': td_form, 'data': test_datas})
    
    td_form.save()
    return HttpResponseRedirect(reverse("test_data"))

def remove_test_data(request, test_data):
    test_data = get_object_or_404(TestData, pk=test_data)
    test_data.delete()
    
    return HttpResponseRedirect(reverse("test_data"))

def test_data_results(request):
    test_datas = TestData.objects.all()
    
    stats = {
        'rugby_tweets': 0,
        'non_rugby': 0,
        'success_rugby': 0,
        'success_non_rugby': 0,
        'rugby_percent': 0,
        'non_rugby_percent': 0,
    }
    
    results = []
    for instance in test_datas:
        matches, confidence = Keyword.match(instance.text)
        if instance.positive:
            stats['rugby_tweets'] = stats['rugby_tweets'] + 1
        else:
            stats['non_rugby'] = stats['non_rugby'] + 1
        
        if len(matches)>0:
            result = {
                'text': instance.text,
                'matches': matches,
                'confidence': confidence,
                'rugby_tweet': 'Is Rugby Tweet' if instance.positive else 'Random Tweet',
            }
            results.append(result)
            
            if instance.positive:
                stats['success_rugby'] = stats['success_rugby'] + 1
            else:
                stats['success_non_rugby'] = stats['success_non_rugby'] + 1
    
    if stats['rugby_tweets'] > 0:
        stats['rugby_percent'] = (stats['success_rugby'] * 1.0/ stats['rugby_tweets']) * 100
    if stats['non_rugby'] > 0:
        stats['non_rugby_percent'] = (stats['success_non_rugby'] * 1.0/ stats['non_rugby']) * 100
    
    return render(request, 'regex/test_data_results.html', {'results': results, 'stats': stats})
