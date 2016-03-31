# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.CharField(max_length=255)),
                ('full_name', models.CharField(max_length=255)),
                ('phone_number', models.CharField(default=None, max_length=50)),
                ('school_name', models.TextField(default=None)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
