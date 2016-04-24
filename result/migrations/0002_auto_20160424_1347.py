# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentresponse',
            name='marksObtained',
            field=models.DecimalField(default=None, max_digits=5, decimal_places=2),
        ),
    ]
