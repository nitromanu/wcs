# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0003_feedback'),
    ]

    operations = [
        migrations.CreateModel(
            name='monthlyReport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('report_id', models.CharField(max_length=255)),
                ('qsets_include', models.TextField(default=None)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
