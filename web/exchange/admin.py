from django.contrib import admin

from .models import (
    FuturesHistory,
    FuturesOrders,
    Portfolio,
    SpotOrders,
    TradeHistory,
    visitor,
)

admin.site.site_header = "Demo Exchange Admin"


class TradeHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "type",
        "pair",
        "amount",
        "price",
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


class visitorAdmin(admin.ModelAdmin):
    list_display = ("ip_address", "humanizeTime", "userAgent", "path", "isAdminPanel")
    list_filter = ("ip_address", "time", "isAdminPanel")
    search_fields = ("userAgent",)


admin.site.register(visitor, visitorAdmin)


class SpotOrdersAdmin(admin.ModelAdmin):
    list_display = (
        "usr",
        "type",
        "pair",
        "amount",
        "price",
        "mortgage",
        "humanizeTime",
    )
    list_filter = (
        "usr",
        "type",
        "pair",
        "mortgage",
    )


admin.site.register(SpotOrders, SpotOrdersAdmin)


class FuturesOrdersAdmin(admin.ModelAdmin):
    list_display = (
        "usr",
        "type",
        "pair",
        "amount",
        "entryPrice",
        "marketPrice",
        "liqPrice",
        "leverage",
        "orderType",
        "marginType",
        "complete",
        "pnl",
        "triggerConditions",
        "humanizeTime",
    )
    list_filter = (
        "usr",
        "type",
        "pair",
        "entryPrice",
        "marketPrice",
        "liqPrice",
        "leverage",
        "orderType",
        "marginType",
        "complete",
        "pnl",
        "triggerConditions",
    )


admin.site.register(FuturesOrders, FuturesOrdersAdmin)


class FuturesHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "orderDetails",
        "histAmount",
        "humanizeTime",
    )
    list_filter = ("orderDetails",)


admin.site.register(FuturesHistory, FuturesHistoryAdmin)
