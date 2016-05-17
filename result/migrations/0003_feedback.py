# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0002_auto_20160424_1347'),
    ]

    operations = [
        migrations.CreateModel(
            name='feedback',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('username', models.CharField(max_length=255)),
                ('question_set', models.CharField(max_length=255)),
                ('feedback', models.TextField(default=None)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
