from django.db import models


class TradeHistory(models.Model):
	id = models.AutoField(primary_key=True)
	type = models.CharField(max_length=4)
	pair = models.CharField(max_length=10, default=None)
	pairPrice = models.FloatField()
	amount = models.FloatField(default=0)
	price = models.FloatField()
	timeStamp = models.FloatField()


class Portfolio(models.Model):
	cryptoName = models.CharField(max_length=10, default=None, primary_key=True)
	amount = models.FloatField(default=0, null=True)
	equivalentAmount = models.FloatField(default=0, null=True)



