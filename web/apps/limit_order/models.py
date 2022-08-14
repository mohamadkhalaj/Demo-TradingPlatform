import requests
from django.conf import settings
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db import models


# only for open spot orders
class LimitOrders(models.Model):
    usr = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    type = models.CharField(max_length=4)
    pair = models.CharField(max_length=20)
    amount = models.CharField(max_length=10)
    pairPrice = models.FloatField(null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True)

    @property
    def get_dollar_equivalent(self):
        base = self.pair.split('-')[0]
        amount = self.amount.split(' ')[0]
        response = requests.get(
            f"https://min-api.cryptocompare.com/data/price?fsym={base}&tsyms=USDT"
        ).json()
        price = float(response['USDT'])

        return price * float(amount)

    @property
    def get_amount(self):
        base = self.pair.split('-')[0]
        amount = self.amount.split(' ')[0]
        pairPrice = self.get_dollar_equivalent
        if base == self.amount.split(' ')[1]:
            return float(amount) * pairPrice
        else:
            return float(amount) / pairPrice

    class Meta:
        verbose_name_plural = "Limit Orders"

    def humanizeTime(self):
        return naturaltime(self.time)

    humanizeTime.short_description = "Time"

    def __str__(self):
        return f"{self.usr} {self.pair}-Limit"