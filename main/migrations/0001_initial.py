# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AdditionalUserInfo'
        db.create_table(u'main_additionaluserinfo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('male', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('female', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('spamCount', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'main', ['AdditionalUserInfo'])

        # Adding model 'Report'
        db.create_table(u'main_report', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('review', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['review.Review'])),
        ))
        db.send_create_signal(u'main', ['Report'])


    def backwards(self, orm):
        # Deleting model 'AdditionalUserInfo'
        db.delete_table(u'main_additionaluserinfo')

        # Deleting model 'Report'
        db.delete_table(u'main_report')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'main.additionaluserinfo': {
            'Meta': {'object_name': 'AdditionalUserInfo'},
            'female': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'male': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'spamCount': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'main.report': {
            'Meta': {'object_name': 'Report'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'review': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['review.Review']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'review.review': {
            'Meta': {'object_name': 'Review'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rank': ('django.db.models.fields.SmallIntegerField', [], {}),
            'toilet': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['toilet.Toilet']"}),
            'up_down_rank': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'review_creator'", 'to': u"orm['auth.User']"})
        },
        u'toilet.toilet': {
            'Meta': {'object_name': 'Toilet'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'female': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '6'}),
            'lng': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '6'}),
            'male': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'numberOfReviews': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rating': ('django.db.models.fields.DecimalField', [], {'default': '5.0', 'max_digits': '11', 'decimal_places': '10'})
        }
    }

    complete_apps = ['main']