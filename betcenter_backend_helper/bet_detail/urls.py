#coding=utf-8

from django.conf.urls import url
from . import apis

urlpatterns = [
        # Query query_bet_detail_by_txhash_api
        url(r'^query/bet/detail/$$', apis.query_bet_detail_by_txhash_api, name="query_bet_detail_by_txhash_api"),
        url(r'^query/bet/detail/by/address/$$', apis.query_bet_detail_by_address_api, name='query_bet_detail_by_address_api'),
        ]

