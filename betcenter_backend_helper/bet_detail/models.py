#coding=utf-8


import json

from django.db import models
from django.conf import settings
from django.core import serializers

from utils.basemodel.base import BaseModel

class BetDetail(BaseModel):

    creater_address = models.CharField(max_length=70, default='')
    tx_hash = models.CharField(max_length=88, primary_key=True)
    category = models.CharField(max_length=20, null=True, blank=True)
    game_id = models.IntegerField(null=True,blank=True)
    minimumbet = models.CharField(max_length=30)
    spread = models.CharField(max_length=30)
    left_odds = models.IntegerField(null=True,blank=True)
    middle_odds = models.IntegerField(null=True,blank=True)
    right_odds = models.IntegerField(null=True,blank=True)
    flag = models.IntegerField(null=True,blank=True)
    time_stamp = models.CharField(max_length=30)
    confirmations = models.IntegerField(null=True,blank=True)
    network_id = models.IntegerField(default=1)




def format_bet_details(details):
    return [o.get_json() for o in details]


