# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-04 17:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ipsaggregator', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shipment',
            name='processed',
            field=models.BooleanField(default=False),
        ),
    ]
