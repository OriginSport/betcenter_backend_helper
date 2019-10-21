# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-10-17 14:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dice', '0010_auto_20181012_1015'),
    ]

    operations = [
        migrations.CreateModel(
            name='Refund',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now_add=True)),
                ('address_from', models.CharField(max_length=42)),
                ('address_to', models.CharField(max_length=42)),
                ('amount', models.BigIntegerField()),
                ('commit', models.CharField(max_length=66)),
                ('transactionHash', models.CharField(max_length=66)),
                ('contract_address', models.CharField(default='', max_length=88)),
                ('network_id', models.IntegerField(default=1)),
                ('time_stamp', models.CharField(blank=True, max_length=20, null=True)),
                ('time', models.DateTimeField(db_index=True, default=None, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]