# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-25 16:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bet_record', '0003_betrecord_game_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='betrecord',
            name='date',
        ),
        migrations.AddField(
            model_name='betrecord',
            name='time_stamp',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
