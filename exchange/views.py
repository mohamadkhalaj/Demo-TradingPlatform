from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import get_user_model
from .common_functions import Give_equivalent
from .models import TradeHistory, Portfolio
from django.shortcuts import render
from .trade import Trade
import json, re


def home(request):
	return render(request, 'exchange/index.html')


def signUp(request):
	return render(request, 'registration/signup.html')

def markets(request):
	return render(request, 'exchange/markets.html')

def symbolInfo(request):
	return render(request, 'exchange/symbol-info.html')

def heatMap(request):
	return render(request, 'exchange/heatmap.html')

@login_required()
def trade(request, value):
	value = re.sub('\'', '\"', value)
	value = json.loads(value)

	# Portfolio.objects.filter(usr=request.user).get(cryptoName='BTC').delete()
	tradeObject = Trade(request.user, value['type'], value['pair'], float(value['amount']))
	result = tradeObject.result

	# newObj = Portfolio(usr=request.user, cryptoName='USDT', amount=1000.0, equivalentAmount=None).save()

	# User.objects.get(username='ali').delete()
	# Portfolio(usr=request.user, cryptoName='BTC', amount=1.2, equivalentAmount=66000).save()

	return JsonResponse(result)
	# return HttpResponse(str(request.user))


@login_required()
def portfolio(request):
	eq = Give_equivalent()
	resJson = dict()
	for index, item in enumerate(Portfolio.objects.filter(usr=request.user).iterator()):
		if item.cryptoName == 'USDT':
			equivalentAmount = None
		else:
			equivalentAmount = eq.calc_equivalent(item.cryptoName, 'USDT', item.amount)[1]
		resJson[index] = {'cryptoName': item.cryptoName, 'amount': item.amount, 'equivalentAmount': equivalentAmount}
	return JsonResponse(resJson)


@login_required()
def tradinghistory(request):
	resJson = dict()
	for index, item in enumerate(TradeHistory.objects.filter(usr=request.user).iterator()):
		resJson[index] = {'type': item.type, 'pair': item.pair, 'pairPrice': item.pairPrice, 'amount': item.amount,'price': item.price, 'timeStamp': item.time}
	return JsonResponse(resJson)
