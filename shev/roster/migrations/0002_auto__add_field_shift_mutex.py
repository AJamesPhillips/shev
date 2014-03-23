# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ShiftType.mutex'
        db.add_column(u'roster_shifttype', 'mutex',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'ShiftType.mutex'
        db.delete_column(u'roster_shifttype', 'mutex')


    models = {
        u'roster.day': {
            'Meta': {'object_name': 'Day'},
            'day': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'roster.outcome': {
            'Meta': {'object_name': 'Outcome'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'})
        },
        u'roster.person': {
            'Meta': {'object_name': 'Person'},
            'band': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'team_or_agency': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['roster.TeamOrAgency']"})
        },
        u'roster.shift': {
            'Meta': {'object_name': 'Shift'},
            'assigned': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'contract': ('django.db.models.fields.CharField', [], {'default': "'REGU'", 'max_length': '4'}),
            'day': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'shifts'", 'to': u"orm['roster.Day']"}),
            'end': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'hours': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'outcome': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['roster.Outcome']", 'null': 'True', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'shifts'", 'to': u"orm['roster.Person']"}),
            'shift_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'shifts'", 'to': u"orm['roster.ShiftType']"}),
            'start': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'supernumerary': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'roster.shifttype': {
            'Meta': {'object_name': 'ShiftType'},
            'clinical': ('django.db.models.fields.BooleanField', [], {}),
            'end': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'hours': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'mutex': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'start': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'supernumeraryable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'time_of_day': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'})
        },
        u'roster.teamoragency': {
            'Meta': {'object_name': 'TeamOrAgency'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        }
    }

    complete_apps = ['roster']