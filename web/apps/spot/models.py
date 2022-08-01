from django.conf import settings
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db import models


# only for open spot orders
class SpotOrders(models.Model):
    usr = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    type = models.CharField(max_length=4)  # buy/sell
    pair = models.CharField(max_length=20)
    amount = models.FloatField()
    price = models.FloatField()
    pairPrice = models.FloatField(null=True)
    mortgage = models.FloatField(blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Spot Orders"

    def humanizeTime(self):
        return naturaltime(self.time)

    humanizeTime.short_description = "Time"

    def __str__(self):
        return f"{self.usr} {self.pair}-SPOT"
