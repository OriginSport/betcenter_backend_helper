# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-11 14:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bet', '0002_auto_20180607_1852'),
    ]

    operations = [
        migrations.AddField(
            model_name='betitem',
            name='contract',
            field=models.CharField(default='', max_length=42),
        ),
        migrations.AddField(
            model_name='betitem',
            name='network_id',
            field=models.IntegerField(default=3),
        ),
    ]
