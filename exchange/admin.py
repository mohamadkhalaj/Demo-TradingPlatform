from django.contrib import admin
from .models import Portfolio, TradeHistory


class TradeHistoryAdmin(admin.ModelAdmin):
	list_display = ('type', 'pair', 'pairPrice', 'amount', 'price', 'time')


admin.site.register(TradeHistory, TradeHistoryAdmin)


class PortfolioAdmin(admin.ModelAdmin):
	list_display = ('cryptoName', 'amount', 'equivalentAmount')


admin.site.register(Portfolio, PortfolioAdmin)
