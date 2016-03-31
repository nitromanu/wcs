# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='questions',
            name='is_active',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='questions',
            name='endDate',
            field=models.DateField(default=None),
        ),
        migrations.AlterField(
            model_name='questions',
            name='startDate',
            field=models.DateField(default=None),
        ),
    ]
