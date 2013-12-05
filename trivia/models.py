__author__ = 'mbacho'

from hashlib import sha1 as sh
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

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
    questions_solved = models.PositiveIntegerField(default=0)
    correct_questions = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return "{0}  {1} points".format(self.user.username, self.points)


class OpenTrivia(models.Model):
    """Stores currently running trivias"""
    user = models.ForeignKey(User)
    trivia_hash = models.CharField(max_length=64, unique=True)
    created = models.DateTimeField(auto_now_add=True, default=timezone.now) #TODO clear out old opentrivias

    @staticmethod
    def gen_hash():
        cur_date = datetime.now()
        hash = sh(str(cur_date))
        return hash.hexdigest()

    def __unicode__(self):
        return "{0} started {1}... on {2}".format(self.user, self.trivia_hash[:5], self.created)

