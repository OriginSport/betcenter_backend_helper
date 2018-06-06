#coding=utf-8

from django.contrib import admin

from .models import BetItem

class BetItemAdmin(admin.ModelAdmin):
    list_display = ("address", "start_time", "date", "category", "deposit")
    list_filter = ("category", )

admin.site.register(BetItem, BetItemAdmin)
