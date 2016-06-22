# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0002_paymentvoucher_number_of_days'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentvoucher',
            name='total_attempts',
            field=models.IntegerField(default=4),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='subscriptiondetails',
            name='attempts_remaining',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
