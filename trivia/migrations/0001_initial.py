# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ChoiceCategory'
        db.create_table(u'trivia_choicecategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
        ))
        db.send_create_signal(u'trivia', ['ChoiceCategory'])

        # Adding model 'Choice'
        db.create_table(u'trivia_choice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['trivia.ChoiceCategory'])),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'trivia', ['Choice'])

        # Adding model 'QuestionLevel'
        db.create_table(u'trivia_questionlevel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
        ))
        db.send_create_signal(u'trivia', ['QuestionLevel'])

        # Adding model 'Question'
        db.create_table(u'trivia_question', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content', self.gf('django.db.models.fields.CharField')(unique=True, max_length=500)),
            ('correct_choice', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['trivia.Choice'])),
            ('level', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['trivia.QuestionLevel'])),
        ))
        db.send_create_signal(u'trivia', ['Question'])


    def backwards(self, orm):
        # Deleting model 'ChoiceCategory'
        db.delete_table(u'trivia_choicecategory')

        # Deleting model 'Choice'
        db.delete_table(u'trivia_choice')

        # Deleting model 'QuestionLevel'
        db.delete_table(u'trivia_questionlevel')

        # Deleting model 'Question'
        db.delete_table(u'trivia_question')


    models = {
        u'trivia.choice': {
            'Meta': {'object_name': 'Choice'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trivia.ChoiceCategory']"}),
            'content': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'trivia.choicecategory': {
            'Meta': {'object_name': 'ChoiceCategory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'})
        },
        u'trivia.question': {
            'Meta': {'object_name': 'Question'},
            'content': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '500'}),
            'correct_choice': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trivia.Choice']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trivia.QuestionLevel']"})
        },
        u'trivia.questionlevel': {
            'Meta': {'object_name': 'QuestionLevel'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'})
        }
    }

    complete_apps = ['trivia']