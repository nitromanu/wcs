# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_feedback'),
    ]

    operations = [
        migrations.RenameField(
            model_name='feedback',
            old_name='feeback',
            new_name='feedback',
        ),
    ]
