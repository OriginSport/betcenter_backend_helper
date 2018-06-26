#coding=utf-8

from django.contrib import admin

from .models import BetDetail, format_bet_details

class BetDetailAdmin(admin.ModelAdmin):
    list_display = ('tx_hash', "left_odds", "middle_odds", "right_odds", "minimumbet", "game_id")
    list_filter = ("tx_hash", )

admin.site.register(BetDetail, BetDetailAdmin)
