from account.models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from exchange.models import Portfolio, TradeHistory

admin.site.register(User, UserAdmin)


class TradeHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "type",
        "pair",
        "amount",
        "humanizeTime",
        "usr",
        "orderType",
        "complete",
    )
    list_filter = ("type", "pair", "usr", "orderType", "complete")


admin.site.register(TradeHistory, TradeHistoryAdmin)


class PortfolioAdmin(admin.ModelAdmin):
    list_display = ("cryptoName", "amount", "usr", "marketType", "equivalentAmount")
    list_filter = ("cryptoName", "usr", "marketType")


admin.site.register(Portfolio, PortfolioAdmin)
