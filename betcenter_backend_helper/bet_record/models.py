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
    time_stamp = models.CharField(max_length=20, null=True, blank=True)
    time =  models.DateTimeField(null=True, db_index=True, default=None)
    tx_hash = models.CharField(max_length=88, default='')
    to = models.CharField(max_length=42)
    quantity = models.CharField(max_length=30)
    network_id = models.IntegerField(default=1)
    game_id = models.IntegerField(null=True,blank=True)
    main_contract_txhash = models.CharField(max_length=88, default='')
    choice = models.CharField(max_length=3, default='')


    





def format_bet_records(records):
    return [o.get_json() for o in records]


