# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='averageResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('categoryCode', models.CharField(max_length=255)),
                ('questionSetID', models.CharField(max_length=255)),
                ('attendedAvg', models.IntegerField(default=0)),
                ('correctAvg', models.IntegerField(default=0)),
                ('wrongAvg', models.IntegerField(default=0)),
                ('timeAvg', models.IntegerField(default=0)),
                ('marksAvg', models.IntegerField(default=0)),
                ('lastSynced', models.DateField(default=None)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='studentResponse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=255)),
                ('categoryCode', models.CharField(max_length=255)),
                ('questionSetID', models.CharField(max_length=255)),
                ('response', models.TextField(default=None)),
                ('sectionResults', models.TextField(default=None)),
                ('marksObtained', models.IntegerField(default=None)),
                ('totalCorrectAnswer', models.IntegerField(default=None)),
                ('totalWrongAnswer', models.IntegerField(default=None)),
                ('totalTimeTaken', models.IntegerField(default=None)),
                ('totalUnAttempted', models.IntegerField(default=None)),
                ('totalAttempted', models.IntegerField(default=None)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
