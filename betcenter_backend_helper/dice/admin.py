#coding=utf-8

from django.contrib import admin

# Register your models here.
from .models import DiceRecord, Refund


#@admin.register(DiceRecord)
class DiceRecordAdmin(admin.ModelAdmin):
    list_display = ('time', 'modulo', 'jackpot_payment', 'choice', 'result', 'network_id')
    list_filter = ('time', 'modulo',)

admin.site.register(DiceRecord, DiceRecordAdmin)


class RefundAdmin(admin.ModelAdmin):
    list_display = ('time', 'network_id', 'amount', 'transactionHash')
    list_filter = ('network_id',)

admin.site.register(Refund, RefundAdmin)
