from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db import models


class visitor(models.Model):
    ip_address = models.GenericIPAddressField()
    time = models.DateTimeField(auto_now=True)
    userAgent = models.CharField(max_length=256, null=True)
    path = models.CharField(max_length=256, null=True)
    isAdminPanel = models.BooleanField(default=False)

    def humanizeTime(self):
        return naturaltime(self.time)

    humanizeTime.short_description = "Time"

    def __str__(self):
        return f"{self.ip_address}, {self.userAgent}"
