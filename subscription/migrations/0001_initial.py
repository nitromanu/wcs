# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='paymentVoucher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category_code', models.CharField(max_length=255)),
                ('voucher_number', models.CharField(max_length=255)),
                ('voucher_price', models.IntegerField()),
                ('created_date', models.DateField(default=None)),
                ('expiry_date', models.DateField(default=None)),
                ('is_active', models.IntegerField(default=1)),
                ('voucher_agent_code', models.CharField(max_length=255)),
                ('used_by', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='subscriptionDetails',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=255)),
                ('start_date', models.DateField(default=None)),
                ('end_date', models.DateField(default=None)),
                ('voucher_number', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
