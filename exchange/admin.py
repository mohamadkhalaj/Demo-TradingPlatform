from django.contrib import admin
from .models import Portfolio, TradeHistory, SpotOrders, FuturesOrders, FuturesHistory


class TradeHistoryAdmin(admin.ModelAdmin):
	list_display = ('type', 'pair','histAmount', 'amount', 'price', 'time', 'usr', 'orderType', 'complete')
admin.site.register(TradeHistory, TradeHistoryAdmin)


class PortfolioAdmin(admin.ModelAdmin):
	list_display = ('cryptoName', 'amount', 'usr', 'marketType')
admin.site.register(Portfolio, PortfolioAdmin)