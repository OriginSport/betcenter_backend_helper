#coding=utf-8

from django.contrib import admin

from .models import BetRecord

class BetRecordAdmin(admin.ModelAdmin):
    list_display = ('tx_hash', "address", "time", "to", "quantity")
    list_filter = ("address", )

admin.site.register(BetRecord, BetRecordAdmin)
