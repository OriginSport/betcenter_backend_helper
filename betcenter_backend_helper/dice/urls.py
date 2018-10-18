#coding=utf-8

from django.conf.urls import url
from . import apis


urlpatterns = [
        url(r'^query/dice/record/$$', apis.query_dice_record_by_address_api, name='query_dice_record_by_address_api'),
        url(r'^query/dice/rank/$$', apis.query_max_win_player_api, name='query_max_win_player_api'),
        url(r'^query/dice/refund/$$', apis.query_refund_by_address_api, name='uery_refund_by_address_api'),
        url(r'^query/dice/bet/$$', apis.query_bet_by_address_api, name='apis.query_bet_by_address_api'),
        ]
