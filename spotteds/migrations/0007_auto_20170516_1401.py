# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-16 17:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spotteds', '0006_auto_20170207_2241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pendingspotted',
            name='api_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='spotted',
            name='api_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='spotted',
            name='reported',
            field=models.CharField(default='', max_length=1000),
        ),
    ]
