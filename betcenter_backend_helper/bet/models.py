#coding=utf-8
"""
Xiubi Charge
"""
__author__ = 'slide'

import json

from django.db import models
from django.conf import settings
from django.core import serializers

from utils.basemodel.base import BaseModel

class BetItem(BaseModel):

    address = models.CharField(max_length=42, primary_key=True)
    category = models.CharField(max_length=42)
    date = models.CharField(max_length=10)
    start_time = models.DateTimeField()
    deposit = models.IntegerField()

    def __str__(self):
        return 'BetItem:%s' % (self.address)

    def get_full_json(self, clean=True):
        serials = serializers.serialize("json", [self])
        struct = json.loads(serials)
        data = struct[0]['fields']
        if 'pk' in struct[0]:
             data['address'] = struct[0]['pk']
        if clean:
            data.pop('create_time')
            data.pop('update_time')
            data.pop('is_active')
        
        return data

def format_bet_items(items):
    return [o.get_full_json() for o in items]
