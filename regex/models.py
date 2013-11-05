import re

from django.db import models

class Keyword(models.Model):
    value = models.CharField(max_length=50, unique=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        ''' shows the keywords value when printing the object '''
        return self.value

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
        if regex:
            matcher = re.compile(regex, re.IGNORECASE)
            # TODO cache matcher

            return matcher.findall(sample)
        
        return list()
