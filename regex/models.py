from __future__ import division

import re
from django.db import models

class Keyword(models.Model):
    value = models.CharField(max_length=50, unique=True)
    date_added = models.DateTimeField(auto_now_add=True)
    weight = models.DecimalField(max_digits=5, decimal_places=4)

    def __unicode__(self):
        ''' shows the keywords value when printing the object '''
        return "%s - %s" % (self.value, repr(self.weight))

    @classmethod
    def regex(self):
        ''' returns a regex OR of all the keywords '''
        named_kwd = lambda i, v: "(?P<i%i>%s)" % (i,v)
        keywords = [named_kwd(keyword.id, keyword.value) for keyword in Keyword.objects.all()]
        if len(keywords) < 1:
            return None
        
        if len(keywords)>100:
            regex = []
            count = 0
            for i in range(0, int(len(keywords)/90)):
                regex.append("|".join(keywords[count:count+90]))
                count = count + 90
            
            regex.append("|".join(keywords[count:]))
            return regex
        
        regex = "|".join(keywords)
        return regex
    
    @classmethod
    def match(self, sample):
        ''' returns a list of words that match the regex of all keywords 
        against the sample '''
        regex = Keyword.regex()
        
        if not regex:
            return list(), 0.0
        
        matchers = []
        if type(regex) == type(list()):
            for r in regex:
                matchers.append(re.compile(r, re.IGNORECASE))
        else:
            matchers.append(re.compile(regex, re.IGNORECASE))
        
        # TODO cache matcher

        results = {}
        for matcher in matchers:
            for m in matcher.finditer(sample):
                results.update([i for i in m.groupdict().items() if i[1]])
        
        matches = results.values()
        if len(matches) < 1:
            return list(), 0.0
        
        match_weights = [Keyword.objects.get(pk=int(m[1:])).weight for m in results.keys()]
        average = sum(match_weights)/len(match_weights)
        return matches, average

class TestData(models.Model):
    text = models.TextField()
    positive = models.BooleanField(default=False)
