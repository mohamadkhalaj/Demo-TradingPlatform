from django.contrib.humanize.templatetags.humanize import naturaltime
from email.policy import default
from statistics import mode
from django.db import models
from django.conf import settings
# from django.conf import DEFAULT_CONTENT_TYPE_DEPRECATED_MSG

class Portfolio(models.Model):
	usr = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	cryptoName = models.CharField(max_length=50)
	amount = models.FloatField(default=0, null=True)
	equivalentAmount = models.FloatField(default=0, null=True, blank=True)
	marketType = models.CharField(max_length=10, default='spot') # spot/futures

	def __str__(self):
		return f'{self.usr} {self.cryptoName}'
	

# details of terminated spot orders
class TradeHistory(models.Model):
	usr = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	type = models.CharField(max_length=4) # buy/sell
	pair = models.CharField(max_length=20)
	pairPrice = models.FloatField()
	orderType = models.CharField(max_length=15, default=None) # market/limit
	histAmount = models.JSONField(default=None)
	amount = models.FloatField()
	price = models.FloatField()
	time = models.DateTimeField(auto_now=True)
	complete = models.BooleanField(default=True)

	def humanizeTime(self):
		return naturaltime(self.time)
	humanizeTime.short_description = 'Time'

	def __str__(self):
		return f'{self.usr} {self.pair}'

	class Meta:
		verbose_name_plural = 'Trade histories'

# only for open spot orders
class SpotOrders(models.Model):
	usr = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	type = models.CharField(max_length=4) # buy/sell
	pair = models.CharField(max_length=20)
	amount = models.FloatField() 
	price = models.FloatField()
	pairPrice = models.FloatField(null=True)
	mortgage = models.FloatField(blank=True, null=True)
	time = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name_plural = 'Spot Orders'

	def humanizeTime(self):
		return naturaltime(self.time)
	humanizeTime.short_description = 'Time'

	def __str__(self):
		return f'{self.usr} {self.pair}-SPOT'

# details of all futures orders
class FuturesOrders(models.Model):
	usr = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	type = models.CharField(max_length=4) # short/long
	pair = models.CharField(max_length=20)
	amount = models.CharField(max_length=100) # e.g., 0.02 BTC
	entryPrice = models.FloatField()
	marketPrice = models.FloatField()
	liqPrice = models.FloatField()
	leverage = models.IntegerField()
	orderType = models.CharField(max_length=15) # market/limit/stop-limit
	marginType = models.CharField(max_length=10) # cross/isolated
	complete = models.BooleanField(default=False)
	pnl = models.FloatField(default=0)
	triggerConditions = models.FloatField(blank=True, null=True) # only used for stop-limit
	createDate = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name_plural = 'Futures Orders'

	def humanizeTime(self):
		return naturaltime(self.createDate)
	humanizeTime.short_description = 'Time'

	def __str__(self):
		return f'{self.usr} {self.pair}-FUTURES'

# extra details for terminated futures orders including history amounts for statistical reports
class FuturesHistory(models.Model):
	orderDetails = models.OneToOneField(FuturesOrders, on_delete=models.DO_NOTHING)
	histAmount = models.JSONField(default=None)
	terminateDate = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name_plural = 'Future histories'

	def humanizeTime(self):
		return naturaltime(self.terminateDate)
	humanizeTime.short_description = 'Time'

	def __str__(self):
		return f'{self.orderDetails}'

class visitor(models.Model):
	ip_address = models.GenericIPAddressField()
	time = models.DateTimeField(auto_now=True)
	userAgent = models.CharField(max_length=256, null=True)
	path = models.CharField(max_length=256, null=True)
	isAdminPanel = models.BooleanField(default=False)

	def humanizeTime(self):
		return naturaltime(self.time)
	humanizeTime.short_description = 'Time'

	def __str__(self):
		return f'{self.ip_address}, {self.userAgent}'