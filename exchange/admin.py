from django.contrib import admin
from .models import Portfolio, TradeHistory


class TradeHistoryAdmin(admin.ModelAdmin):
	list_display = ('type', 'pair','histAmount', 'amount', 'price', 'time', 'usr')
admin.site.register(TradeHistory, TradeHistoryAdmin)


class PortfolioAdmin(admin.ModelAdmin):
	list_display = ('cryptoName', 'amount', 'usr')
admin.site.register(Portfolio, PortfolioAdmin)
