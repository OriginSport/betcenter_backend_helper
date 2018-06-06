#coding=utf-8

from django.conf.urls import url
from . import apis

urlpatterns = [
        # Query
        url(r'^add/bet/$', apis.add_bet_api, name="add_bet_api"),
        # url(r'^query/bet/$', apis.query_all_bet_api, name="query_all_bet_api"),
        url(r'^query/bet/category/$$', apis.query_bet_by_category_api, name="query_bet_by_category_api"),
        ]

