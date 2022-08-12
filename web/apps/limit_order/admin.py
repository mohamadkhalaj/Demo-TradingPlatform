from django.contrib import admin
from .models import LimitOrders


# Register your models here.
class LimitOrdersAdmin(admin.ModelAdmin):
    list_display = (
        "usr",
        "type",
        "pair",
        "amount",
        "humanizeTime",
    )
    list_filter = (
        "usr",
        "type",
        "pair",
    )


admin.site.register(LimitOrders, LimitOrdersAdmin)
