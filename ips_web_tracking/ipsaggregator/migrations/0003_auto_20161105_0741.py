# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-05 07:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ipsaggregator', '0002_shipment_processed'),
    ]

    operations = [
        migrations.AddField(
            model_name='shipment',
            name='info',
            field=models.CharField(blank=True, default='', max_length=4096, null=True),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='identifier',
            field=models.CharField(db_index=True, max_length=255, unique=True),
        ),
    ]
