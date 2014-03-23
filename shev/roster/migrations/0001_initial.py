# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TeamOrAgency'
        db.create_table(u'roster_teamoragency', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=40)),
        ))
        db.send_create_signal(u'roster', ['TeamOrAgency'])

        # Adding model 'Person'
        db.create_table(u'roster_person', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('band', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('team_or_agency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['roster.TeamOrAgency'])),
        ))
        db.send_create_signal(u'roster', ['Person'])

        # Adding model 'ShiftType'
        db.create_table(u'roster_shifttype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('hours', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('start', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('end', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('clinical', self.gf('django.db.models.fields.BooleanField')()),
            ('supernumeraryable', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('time_of_day', self.gf('django.db.models.fields.CharField')(max_length=10, null=True)),
        ))
        db.send_create_signal(u'roster', ['ShiftType'])

        # Adding model 'Outcome'
        db.create_table(u'roster_outcome', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
        ))
        db.send_create_signal(u'roster', ['Outcome'])

        # Adding model 'Day'
        db.create_table(u'roster_day', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('day', self.gf('django.db.models.fields.DateField')()),
            ('note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'roster', ['Day'])

        # Adding model 'Shift'
        db.create_table(u'roster_shift', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('day', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['roster.Day'])),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['roster.Person'])),
            ('shift_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['roster.ShiftType'])),
            ('supernumerary', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('start', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('end', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('hours', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('contract', self.gf('django.db.models.fields.CharField')(default='REGU', max_length=4)),
            ('outcome', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['roster.Outcome'])),
            ('note', self.gf('django.db.models.fields.CharField')(max_length=80, null=True, blank=True)),
            ('assigned', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
        ))
        db.send_create_signal(u'roster', ['Shift'])


    def backwards(self, orm):
        # Deleting model 'TeamOrAgency'
        db.delete_table(u'roster_teamoragency')

        # Deleting model 'Person'
        db.delete_table(u'roster_person')

        # Deleting model 'ShiftType'
        db.delete_table(u'roster_shifttype')

        # Deleting model 'Outcome'
        db.delete_table(u'roster_outcome')

        # Deleting model 'Day'
        db.delete_table(u'roster_day')

        # Deleting model 'Shift'
        db.delete_table(u'roster_shift')


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
            'day': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['roster.Day']"}),
            'end': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'hours': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'outcome': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['roster.Outcome']"}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['roster.Person']"}),
            'shift_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['roster.ShiftType']"}),
            'start': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'supernumerary': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'roster.shifttype': {
            'Meta': {'object_name': 'ShiftType'},
            'clinical': ('django.db.models.fields.BooleanField', [], {}),
            'end': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'hours': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
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