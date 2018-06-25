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
from .models import BetRecord, format_bet_records


logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)


class QueryBetRecordByAddressAPI(AbstractAPI):
    def config_args(self):
        self.args = {
                'address': 'r',
                'network_id': 'r',
                'category': ('o', None),
                }

    def access_db(self, kwarg):
        category = kwarg['category']
        network_id = kwarg['network_id']
        address = kwarg['address']

        brs = BetRecord.objects.filter(address=address, network_id=network_id).all().order_by('-date')

        data = format_bet_records(brs)
        return True, data


    def format_data(self, data):
        if data[0]:
            return ok_json(data[1])
        return fail_json(err.ERROR_CODE_DATABASE_QUERY_ERROR)


query_bet_record_by_address_api = QueryBetRecordByAddressAPI().wrap_func()







