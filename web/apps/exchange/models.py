import requests
from django.conf import settings
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db import models


class Portfolio(models.Model):
    MARKET_TYPES = (
        ("spot", "spot"),
        ("futures", "futures")
    )
    usr = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cryptoName = models.CharField(max_length=255)
    amount = models.FloatField(default=0, null=True)
    equivalentAmount = models.FloatField(default=0, null=True, blank=True)
    marketType = models.CharField(max_length=10, default="spot", choices=MARKET_TYPES)

    def __str__(self):
        return f"{self.usr} {self.cryptoName}"

    @property
    def get_dollar_equivalent(self):
        response = requests.get(
            f"https://min-api.cryptocompare.com/data/price?fsym={self.cryptoName}&tsyms=USDT"
        ).json()
        price = float(response['USDT'])

        return price * self.amount


# details of terminated spot orders
class TradeHistory(models.Model):
    TRADE_TYPES = (
        ("buy", "buy"),
        ("sell", "sell")
    )
    ORDER_TYPES = (
        ("market", "market"),
        ("limit", "limit")
    )
    usr = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    type = models.CharField(max_length=4, choices=TRADE_TYPES)
    pair = models.CharField(max_length=255)
    pairPrice = models.FloatField()
    orderType = models.CharField(max_length=15, choices=ORDER_TYPES)
    histAmount = models.JSONField(default=None, blank=True, null=True)
    amount = models.CharField(max_length=255)
    time = models.DateTimeField(auto_now=True)
    complete = models.BooleanField(default=True)

    def humanizeTime(self):
        return naturaltime(self.time)

    humanizeTime.short_description = "Time"

    def __str__(self):
        return f"{self.usr} {self.pair}"

    class Meta:
        verbose_name_plural = "Trade histories"
