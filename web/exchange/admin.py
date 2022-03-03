from django.contrib import admin
from .models import (
		Portfolio, 
		TradeHistory, 
		SpotOrders, 
		FuturesOrders, 
		FuturesHistory, 
		visitor,
	)


class TradeHistoryAdmin(admin.ModelAdmin):
	list_display = (
		'type', 
		'pair', 
		'histAmount', 
		'amount', 
		'price', 
		'humanizeTime', 
		'usr', 
		'orderType', 
		'complete'
	)
admin.site.register(TradeHistory, TradeHistoryAdmin)


class PortfolioAdmin(admin.ModelAdmin):
	list_display = (
		'cryptoName', 
		'amount', 
		'usr', 
		'marketType'
	)
admin.site.register(Portfolio, PortfolioAdmin)

class visitorAdmin(admin.ModelAdmin):
	list_display = (
		'ip_address', 
		'humanizeTime', 
		'userAgent', 
		'path', 
		'isAdminPanel'
	)
	list_filter = (
		'ip_address', 
		'time', 
		'isAdminPanel'
	)
	search_fields = ('userAgent',)
admin.site.register(visitor, visitorAdmin)

class SpotOrdersAdmin(admin.ModelAdmin):
	list_display = (
		'usr', 
		'type', 
		'pair', 
		'orderType', 
		'amount', 
		'price', 
		'triggerConditions', 
		'humanizeTime', 
	)
admin.site.register(SpotOrders, SpotOrdersAdmin)

class FuturesOrdersAdmin(admin.ModelAdmin):
	list_display = (
		'usr', 
		'type', 
		'pair', 
		'amount', 
		'entryPrice', 
		'marketPrice', 
		'liqPrice', 
		'leverage', 
		'orderType',
		'marginType',
		'complete',
		'pnl',
		'triggerConditions',
		'humanizeTime',
	)
admin.site.register(FuturesOrders, FuturesOrdersAdmin)

class FuturesHistoryAdmin(admin.ModelAdmin):
	list_display = (
		'orderDetails', 
		'histAmount', 
		'humanizeTime', 
	)
admin.site.register(FuturesHistory, FuturesHistoryAdmin)