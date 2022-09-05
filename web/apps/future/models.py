from django.conf import settings
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db import models


# Create your models here.
# details of all futures orders
class FuturesOrders(models.Model):
    usr = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    type = models.CharField(max_length=4)  # short/long
    pair = models.CharField(max_length=20)
    amount = models.CharField(max_length=100)  # e.g., 0.02 BTC
    entryPrice = models.FloatField()
    marketPrice = models.FloatField()
    liqPrice = models.FloatField()
    leverage = models.IntegerField()
    orderType = models.CharField(max_length=15)  # market/limit/stop-limit
    marginType = models.CharField(max_length=10)  # cross/isolated
    complete = models.BooleanField(default=False)
    pnl = models.FloatField(default=0)
    triggerConditions = models.FloatField(blank=True, null=True)  # only used for stop-limit
    createDate = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Futures Orders"

    def humanizeTime(self):
        return naturaltime(self.createDate)

    humanizeTime.short_description = "Time"

    def __str__(self):
        return f"{self.usr} {self.pair}-FUTURES"


# extra details for terminated futures orders including history amounts for statistical reports
class FuturesHistory(models.Model):
    orderDetails = models.OneToOneField(FuturesOrders, on_delete=models.DO_NOTHING)
    histAmount = models.JSONField(default=None)
    terminateDate = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Future histories"

    def humanizeTime(self):
        return naturaltime(self.terminateDate)

    humanizeTime.short_description = "Time"

    def __str__(self):
        return f"{self.orderDetails}"
