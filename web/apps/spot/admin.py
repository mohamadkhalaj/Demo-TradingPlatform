from django.contrib import admin

from .models import SpotOrders


# Register your models here.
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
