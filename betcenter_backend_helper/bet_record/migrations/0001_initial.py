# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-20 14:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BetRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now_add=True)),
                ('address', models.CharField(max_length=42)),
                ('category', models.CharField(default='', max_length=42)),
                ('contract', models.CharField(default='', max_length=42)),
                ('date', models.CharField(max_length=10)),
                ('time_str', models.DateTimeField()),
                ('tx_hash', models.CharField(default='', max_length=88)),
                ('to', models.CharField(max_length=42)),
                ('quantity', models.CharField(max_length=22)),
                ('network_id', models.IntegerField(default=3)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
