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
from .models import BetDetail, format_bet_details


logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)


class QueryBetDeatilByTxhashAPI(AbstractAPI):
    def config_args(self):
        self.args = {
                'txhash': 'r',
                'network_id': 'r',
                'category': ('o', None),
                }

    def access_db(self, kwarg):
        category = kwarg['category']
        network_id = kwarg['network_id']
        txhash = kwarg['txhash']

        bds = BetDetail.objects.filter(tx_hash=txhash, network_id=network_id).all().order_by('-time_stamp')

        data = format_bet_details(bds)
        return True, data


    def format_data(self, data):
        if data[0]:
            return ok_json(data[1])
        return fail_json(err.ERROR_CODE_DATABASE_QUERY_ERROR)


query_bet_detail_by_txhash_api = QueryBetDeatilByTxhashAPI().wrap_func()







