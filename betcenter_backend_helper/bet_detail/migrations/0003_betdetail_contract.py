# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-28 09:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bet_detail', '0002_betdetail_creater_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='betdetail',
            name='contract',
            field=models.CharField(default='', max_length=42),
        ),
    ]
