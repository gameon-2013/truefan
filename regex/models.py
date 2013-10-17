import re

from django.db import models

class Keyword(models.Model):
    value = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kargs):
        ''' adds a new compiled regex every time a keyword is saved '''
        super(Keyword, self).save(*args,**kargs)

        CompiledRegex.recompile()

    def delete(self, *args, **kargs):
        ''' adds a new compiled regex every time a keyword is removed '''
        super(Keyword, self).delete(*args, **kargs)

        CompiledRegex.recompile()

    def __unicode__(self):
        ''' shows the keywords value when printing the object '''
        return self.value

class CompiledRegex(models.Model):
    value = models.TextField()
    regex = models.TextField()
    date_compiled = models.DateTimeField(auto_now=True)

    @classmethod
    def recompile(self):
        ''' adds a new compiled regex '''
        keywords = [keyword.value for keyword in Keyword.objects.all()]
        regex = "|".join(keywords)

        compiled = re.compile(regex)

        new_compiled_regex = CompiledRegex(value=compiled, regex=regex)
        new_compiled_regex.save()

    def __unicode__(self):
        ''' shows the compiled regex's original regex when printing the object '''
        return self.regex