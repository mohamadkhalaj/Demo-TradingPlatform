from django.db import models


class TradeHistory(models.Model):
	id = models.AutoField(primary_key=True)
	type = models.CharField(max_length=1)  # s/b
	cryptoName = models.CharField(max_length=10, default=None)
	price = models.CharField(max_length=15)
	date = models.DateField(auto_now=True)
	amount = models.CharField(max_length=15, default='0')
	equivalentAmount = models.CharField(max_length=15, default='0')


class Portfolio(models.Model):
	id = models.AutoField(primary_key=True)
	cryptoName = models.CharField(max_length=10, default=None)
	price = models.CharField(max_length=15)
	date = models.DateField(auto_now=True)
	amount = models.CharField(max_length=15, default='0')
	equivalentAmount = models.CharField(max_length=15, default='0')


