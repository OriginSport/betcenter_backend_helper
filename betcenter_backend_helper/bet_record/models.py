#coding=utf-8


import json

from django.db import models
from django.conf import settings
from django.core import serializers

from utils.basemodel.base import BaseModel

class BetRecord(BaseModel):

    address = models.CharField(max_length=42)
    category = models.CharField(max_length=42, default='')
    contract = models.CharField(max_length=42)
    date = models.CharField(max_length=10)
    #time_str = models.DateTimeField()
    time =  models.DateTimeField()
    tx_hash = models.CharField(max_length=88, default='')
    to = models.CharField(max_length=42)
    quantity = models.CharField(max_length=30)
    network_id = models.IntegerField(default=3)
    game_id = models.IntegerField(null=True,blank=True)
    





def format_bet_records(records):
    return [o.get_json() for o in records]


