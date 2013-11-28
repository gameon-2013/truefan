__author__ = 'mbacho'
from models import Choice
from models import ChoiceCategory
from models import Question
from models import QuestionLevel
from django.contrib import admin
from models import UserPoints
admin.site.register(Choice)
admin.site.register(ChoiceCategory)
admin.site.register(Question)
admin.site.register(QuestionLevel)
admin.site.register(UserPoints)
