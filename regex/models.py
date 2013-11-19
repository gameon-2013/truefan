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
        keywords = [keyword.value for keyword in Keyword.objects.all()]
        if len(keywords) < 1:
            return None
        
        regex = "|".join(keywords)
        return regex

    @classmethod
    def match(self, sample):
        ''' returns a list of words that match the regex of all keywords 
        against the sample '''
        regex = Keyword.regex()
        
        if not regex:
            return list(), 0.0
        
        matcher = re.compile(regex, re.IGNORECASE)
        # TODO cache matcher

        matches = matcher.findall(sample)
        if len(matches) < 1:
            return list(), 0.0
        
        match_weights = [Keyword.objects.get(value__iexact=m).weight for m in matches]
        average = sum(match_weights)/len(match_weights)
        return matches, average
