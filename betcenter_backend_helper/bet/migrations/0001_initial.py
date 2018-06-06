# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-06 16:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BetItem',
            fields=[
                ('is_active', models.BooleanField(default=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now_add=True)),
                ('address', models.CharField(max_length=42, primary_key=True, serialize=False)),
                ('category', models.CharField(max_length=42)),
                ('date', models.CharField(max_length=10)),
                ('start_time', models.DateTimeField()),
                ('deposit', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
