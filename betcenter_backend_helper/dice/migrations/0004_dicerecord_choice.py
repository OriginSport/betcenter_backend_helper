# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-10-10 14:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dice', '0003_dicerecord_result'),
    ]

    operations = [
        migrations.AddField(
            model_name='dicerecord',
            name='choice',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
