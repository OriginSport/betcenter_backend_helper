#coding=utf-8

from django.contrib import admin

# Register your models here.
from .models import DiceRecord


#@admin.register(DiceRecord)
class DiceRecordAdmin(admin.ModelAdmin):
    list_display = ('time', 'modulo', 'jackpot_payment', 'choice', 'result', 'network_id')
    list_filter = ('time', 'modulo',)

admin.site.register(DiceRecord, DiceRecordAdmin)



