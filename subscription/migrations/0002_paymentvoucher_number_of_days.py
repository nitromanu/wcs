# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentvoucher',
            name='number_of_days',
            field=models.IntegerField(default=30),
            preserve_default=True,
        ),
    ]
