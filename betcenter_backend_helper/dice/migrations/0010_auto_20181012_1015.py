# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-10-12 10:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dice', '0009_auto_20181011_1147'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dicerecord',
            old_name='tx_hash',
            new_name='transactionHash',
        ),
        migrations.AlterField(
            model_name='dicerecord',
            name='dice_payment',
            field=models.BigIntegerField(default=0),
        ),
    ]