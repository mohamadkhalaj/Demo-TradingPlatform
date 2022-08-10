from django.contrib import admin

from .models import visitor


class visitorAdmin(admin.ModelAdmin):
    list_display = ("ip_address", "humanizeTime", "userAgent", "path", "isAdminPanel")
    list_filter = ("time", "isAdminPanel")
    search_fields = ("userAgent", "ip_address", "path")


admin.site.register(visitor, visitorAdmin)
