#coding=utf-8

from django.contrib import admin

# Register your models here.
from .models import DiceRecord


#@admin.register(DiceRecord)
class DiceRecordAdmin(admin.ModelAdmin):
    list_display = ('time', 'bet_mask', 'modulo', 'dice_payment', 'jackpot_payment',)
    list_filter = ('time', 'modulo',)

admin.site.register(DiceRecord, DiceRecordAdmin)



