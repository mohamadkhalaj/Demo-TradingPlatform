from django.contrib import admin

from .models import FuturesHistory, FuturesOrders


# Register your models here.
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
