# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-10-10 21:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dice', '0006_auto_20181010_2101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dicerecord',
            name='amount',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='dicerecord',
            name='dice_payment',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='dicerecord',
            name='jackpot_payment',
            field=models.BigIntegerField(),
        ),
    ]
