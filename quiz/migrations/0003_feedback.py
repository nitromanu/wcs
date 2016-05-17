# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_auto_20160331_0821'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=255)),
                ('questionSetID', models.CharField(max_length=255)),
                ('feeback', models.TextField(default=None)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
