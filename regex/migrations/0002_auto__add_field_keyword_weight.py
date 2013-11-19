# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Keyword.weight'
        db.add_column(u'regex_keyword', 'weight',
                      self.gf('django.db.models.fields.DecimalField')(default=0.5, max_digits=5, decimal_places=4),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Keyword.weight'
        db.delete_column(u'regex_keyword', 'weight')


    models = {
        u'regex.keyword': {
            'Meta': {'object_name': 'Keyword'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'weight': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '4'})
        }
    }

    complete_apps = ['regex']