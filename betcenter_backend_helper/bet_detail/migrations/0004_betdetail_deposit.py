# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-28 10:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bet_detail', '0003_betdetail_contract'),
    ]

    operations = [
        migrations.AddField(
            model_name='betdetail',
            name='deposit',
            field=models.CharField(default='', max_length=25),
        ),
    ]
