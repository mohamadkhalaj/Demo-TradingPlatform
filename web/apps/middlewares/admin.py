from django.contrib import admin

from .models import visitor


class visitorAdmin(admin.ModelAdmin):
    list_display = ("ip_address", "humanizeTime", "userAgent", "path", "isAdminPanel")
    list_filter = ("ip_address", "time", "isAdminPanel")
    search_fields = ("userAgent",)


admin.site.register(visitor, visitorAdmin)
