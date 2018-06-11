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
from .models import BetItem, format_bet_items

logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

class AddBetAPI(AbstractAPI):
    def config_args(self):
        self.args = {
                'address': 'r',
                'start_time': 'r',
                'deposit': 'r',
                'category': 'r',
                'contract': 'r',
                'network_id': 'r',
                }

    def access_db(self, kwarg):
        address = kwarg['address']
        start_time = kwarg['start_time']
        deposit = kwarg['deposit']
        category = kwarg['category']
        contract = kwarg['contract']
        network_id = kwarg['network_id']

        bi = BetItem.objects.filter(address=address).first()
        if not bi:
            bi = BetItem()
        bi.address = address
        bi.start_time = datetime.datetime.fromtimestamp(float(start_time))
        bi.deposit = deposit
        bi.category = category
        bi.contract = contract 
        bi.network_id = network_id
        bi.date = datetime.datetime.fromtimestamp(float(start_time)).date().isoformat()[:10]
        bi.save()
        return True, bi.get_full_json()

    def format_data(self, data):
        if data[0]:
            return ok_json(data[1])
        return fail_json(err.ERROR_CODE_DATABASE_QUERY_ERROR)

add_bet_api = AddBetAPI().wrap_func()

class QueryBetByCategoryAPI(AbstractAPI):
    def config_args(self):
        self.args = {
                'category': 'r',
                'contract': 'r',
                'network_id': 'r',
                'date': ('o', None),
                }
    def access_db(self, kwarg):
        category = kwarg['category']
        date = kwarg['date']
        contract = kwarg['contract']
        network_id = kwarg['network_id']

        bis = BetItem.objects.filter(contract=contract, network_id=network_id, category=category).all()
        if date:
            bis = bis.filter(date=date).all()
        bis.order_by('deposit')
        data = format_bet_items(bis)
        return True, data

    def format_data(self, data):
        if data[0]:
            return ok_json(data[1])
        return fail_json(err.ERROR_CODE_DATABASE_QUERY_ERROR)

query_bet_by_category_api = QueryBetByCategoryAPI().wrap_func()
