# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('questionSetID', models.CharField(max_length=255)),
                ('totalQuestions', models.IntegerField()),
                ('questionSections', models.TextField()),
                ('questionsJson', models.TextField()),
                ('totalTime', models.IntegerField(default=60)),
                ('categoryCode', models.CharField(default=None, max_length=255)),
                ('startDate', models.DateField()),
                ('endDate', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
