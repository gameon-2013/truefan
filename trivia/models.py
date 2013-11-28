__author__ = 'mbacho'

from django.db import models
from django.contrib.auth.models import User

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
    points = models.PositiveSmallIntegerField(default=3)

    def __unicode__(self):
        return self.name


class Question(models.Model):
    content = models.CharField(max_length=500, unique=True)
    correct_choice = models.ForeignKey(Choice)
    level = models.ForeignKey(QuestionLevel)


    def __unicode__(self):
        return self.content

class UserPoints(models.Model):
    user = models.OneToOneField(User)
    points = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return "{0}  {1} points".format(self.user.username, self.points)