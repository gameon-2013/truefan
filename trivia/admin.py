__author__ = 'mbacho'
from django.contrib import admin

from trivia.models import Choice
from trivia.models import ChoiceCategory
from trivia.models import Question
from trivia.models import QuestionLevel
from trivia.models import UserPoints
from trivia.models import OpenTrivia


admin.site.register(Choice)
admin.site.register(ChoiceCategory)
admin.site.register(Question)
admin.site.register(QuestionLevel)
admin.site.register(UserPoints)
admin.site.register(OpenTrivia)