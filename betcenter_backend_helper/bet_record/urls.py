#coding=utf-8

from django.conf.urls import url
from . import apis

urlpatterns = [
        # Query query_bet_record_by_address_api
        url(r'^query/bet/record/$$', apis.query_bet_record_by_address_api, name="query_bet_record_by_address_api"),

        ]

