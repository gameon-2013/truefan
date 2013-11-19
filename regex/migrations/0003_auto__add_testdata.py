# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TestData'
        db.create_table(u'regex_testdata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('positive', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'regex', ['TestData'])


    def backwards(self, orm):
        # Deleting model 'TestData'
        db.delete_table(u'regex_testdata')


    models = {
        u'regex.keyword': {
            'Meta': {'object_name': 'Keyword'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'weight': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '4'})
        },
        u'regex.testdata': {
            'Meta': {'object_name': 'TestData'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'positive': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'text': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['regex']