__author__ = 'mbacho'

from django.db import models

# Create your models here.

class ChoiceCategory(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __unicode__(self):
        return self.name


class Choice(models.Model):
    category = models.ForeignKey(ChoiceCategory)
    content = models.CharField(max_length=255)

    def __unicode__(self):
        return self.content


class QuestionLevel(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __unicode__(self):
        return self.name


class Question(models.Model):
    content = models.CharField(max_length=500, unique=True)
    correct_choice = models.ForeignKey(Choice)
    level = models.ForeignKey(QuestionLevel)


    def __unicode__(self):
        return self.content

