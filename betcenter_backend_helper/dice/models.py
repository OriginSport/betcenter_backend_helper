#coding=utf-8

import json
import logging
from django.conf import settings
from django.db import models
import math
from django.db.models.signals import post_save
from utils.basemodel.base import BaseModel
from django.core import serializers

class DiceRecord(BaseModel):
    address_from = models.CharField(max_length=42)
    address_to = models.CharField(max_length=42)
    amount = models.BigIntegerField() #/10^18 投注
    bet_block_hash = models.CharField(max_length=66)
    bet_mask = models.CharField(max_length=4) #%40,%50
    commit = models.CharField(max_length=66) #唯一标识
    dice_payment = models.BigIntegerField(default=0) #预计奖励
    jackpot_payment = models.BigIntegerField() #实际奖励
    modulo = models.CharField(max_length=4) #取模, 2, 6, 12, 100(type)
    reveal = models.CharField(max_length=66)
    reveal_block_hash = models.CharField(max_length=66)
    reveal_tx_hash = models.CharField(max_length=66)
    transactionHash = models.CharField(max_length=66)
    contract_address = models.CharField(max_length=88, default='')# test and online
    network_id = models.IntegerField(default=1)
    time_stamp = models.CharField(max_length=20, null=True, blank=True)
    time = models.DateTimeField(null=True, db_index=True, default=None)
    result = models.CharField(max_length=30, null=True, blank=True)
    choice = models.CharField(max_length=30, null=True, blank=True)

    def get_json(self, clean=True):
        serials = serializers.serialize("json", [self])
        struct = json.loads(serials)
        data = struct[0]['fields']
        if 'pk' in struct[0]:
            data['id'] = struct[0]['pk']
        if clean:
            data.pop('create_time')
            data.pop('update_time')
            data.pop('is_active')
            data.pop('address_to')
            data.pop('bet_block_hash')
            data.pop('bet_mask')
            #data.pop('commit')
            data.pop('dice_payment')
            data.pop('reveal_block_hash')
            data.pop('contract_address')
            data.pop('reveal_tx_hash')
        return data

    



def format_dice_records(records):
    return [o.get_json() for o in records]


class Refund(BaseModel):
    address_from = models.CharField(max_length=42)
    address_to = models.CharField(max_length=42)
    amount = models.BigIntegerField() #/10^18 投注
    commit = models.CharField(max_length=66) 
    transactionHash = models.CharField(max_length=66)
    contract_address = models.CharField(max_length=88, default='')# test and online
    network_id = models.IntegerField(default=1)
    time_stamp = models.CharField(max_length=20, null=True, blank=True)
    time = models.DateTimeField(null=True, db_index=True, default=None)


def format_refunds(refunds):
    return [o.get_json() for o in refunds]




class Bet(BaseModel):
    address_from = models.CharField(max_length=42)
    address_to = models.CharField(max_length=42)
    amount = models.BigIntegerField() #/10^18 投注
    commit = models.CharField(max_length=66) 
    transactionHash = models.CharField(max_length=66)
    contract_address = models.CharField(max_length=88, default='')# test and online
    network_id = models.IntegerField(default=1)
    time_stamp = models.CharField(max_length=20, null=True, blank=True)
    time = models.DateTimeField(null=True, db_index=True, default=None)
    modulo = models.CharField(max_length=4) #取模, 2, 6, 12, 100(type)
    choice = models.CharField(max_length=30, null=True, blank=True)



def format_bets(bets):
    return [o.get_json() for o in bets]








