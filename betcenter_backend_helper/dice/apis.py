#coding=utf-8

import logging
import random
import datetime
import simplejson
from django.conf import settings
from django.db import transaction

import utils.errors as err
from utils.view_tools import ok_json, fail_json, get_real_ip
from utils.abstract_api import AbstractAPI
from .models import DiceRecord, format_dice_records
from utils.paginator import CommonPaginator

import math
import hashlib
import requests
import json

logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)


class QueryDiceRecordByAddressAPI(AbstractAPI):
    def config_args(self):
        self.args = {
                'address': ('o', None),
                'network_id': 'r',
                'type': 'r',
                'page': ('o', 1),
                'page_size': ('o', 20),
                }
    def access_db(self, kwarg):
        network_id = kwarg['network_id']
        address = kwarg['address']
        type = kwarg['type']
        if address:
            drs = DiceRecord.objects.filter(is_active=True,address_from=address, network_id=network_id, modulo=type).all().order_by('-time_stamp')

        else:
            drs = DiceRecord.objects.filter(is_active=True,network_id=network_id, modulo=type).all().order_by('-time_stamp')

        paginator = CommonPaginator(drs, lambda x: format_dice_records(x), int(kwarg['page']), int(kwarg['page_size']), kwarg['request'])


        return paginator

    def format_data(self, data):
        if data:
            return ok_json(data={
                'count': data.count,
                'records': data.entries,
                'page': data.page,
                'page_size': data.page_size,
                'next': data.next,
                'has_next':data.has_next
            })

        return fail_json(err.ERROR_CODE_DATABASE_QUERY_ERROR)


query_dice_record_by_address_api = QueryDiceRecordByAddressAPI().wrap_func()


class QueryMaxWinPlayerAPI(AbstractAPI):
    def config_args(self):
        self.args = {
                'network_id': 'r',
                }
    def access_db(self, kwarg):
        network_id = kwarg['network_id']
        now = datetime.datetime.now()
        date_day = now - datetime.timedelta(hours=24)
        now_str = now.strftime('%Y-%m-%d %H:%M:%S')
        date_day_str = date_day.strftime('%Y-%m-%d %H:%M:%S')

        drs = DiceRecord.objects.filter(is_active=True,network_id=network_id, jackpot_payment__gte=0, time__gte=date_day_str, time__lte=now_str).all().order_by('-jackpot_payment')
        address_list = []
        rank_list = []
        for dr in drs:
            if dr.address_from not in address_list:
                address_list.append(dr.address_from)
                rank_list.append({'address': dr.address_from, 'win_amount': dr.jackpot_payment})
        return True, rank_list[:3]
    def format_data(self, data):
        if data[0]:
            return ok_json(data=data[1])
        return fail_json(err.ERROR_CODE_DATABASE_QUERY_ERROR)


query_max_win_player_api = QueryMaxWinPlayerAPI().wrap_func()



