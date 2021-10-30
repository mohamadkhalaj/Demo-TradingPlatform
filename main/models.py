from django.db import models


class UsrRegistration(models.Model):
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=35)
    nationalId = models.BigIntegerField(primary_key=True)
    address = models.CharField(max_length=250)
    phoneNumber = models.IntegerField()
    mobileNumber = models.BigIntegerField()
    email = models.EmailField()
    password = models.CharField(max_length=35)
    mainBalance = models.CharField(default='1000', max_length=10)


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


