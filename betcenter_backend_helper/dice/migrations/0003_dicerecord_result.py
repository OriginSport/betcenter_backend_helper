# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-10-09 18:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dice', '0002_random'),
    ]

    operations = [
        migrations.AddField(
            model_name='dicerecord',
            name='result',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
