from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import get_user_model
from .common_functions import Give_equivalent, pretify
from .models import TradeHistory, Portfolio
from django.core.paginator import Paginator
from django.shortcuts import render
from .trade import Trade
import json, re, requests
from account.models import User
from django.contrib.auth import get_user_model
from django.conf import settings

def home(request):
	if request.user.is_authenticated:
		obj = User.objects.get(username=request.user)
		if obj.first_login:
			newObj = Portfolio(usr=request.user, cryptoName='USDT', amount=settings.DEFAULT_BALANCE, equivalentAmount=None)
			newObj.save()
			obj.first_login = False
			obj.save()	
	return render(request, 'exchange/index.html')


def signUp(request):
	return render(request, 'registration/signup.html')

def markets(request):
	return render(request, 'exchange/markets.html')

@login_required()
def trade(request, value):
	value = re.sub('\'', '\"', value)
	value = json.loads(value)

	tradeObject = Trade(request.user, 'market', value['type'], value['pair'], value['amount'])
	result = tradeObject.result

	return JsonResponse(result)


@login_required()
def portfolio(request):
	eq = Give_equivalent()
	resJson = dict()
	for index, item in enumerate(Portfolio.objects.filter(usr=request.user).iterator()):
		if item.cryptoName == 'USDT':
			equivalentAmount = None
		else:
			equivalentAmount = eq.calc_equivalent(item.cryptoName, 'USDT', item.amount)[1]
		resJson[index] = {'cryptoName': item.cryptoName, 'amount': item.amount, 'equivalentAmount': equivalentAmount, 'marketType': item.marketType}
	return JsonResponse(resJson)


@login_required()
def tradinghistory(request):
	resJson = dict()

	for index, item in enumerate(TradeHistory.objects.filter(usr=request.user, amount__gt=0).order_by('-time').iterator()):
		resJson[index] = {'type': item.type, 'pair': item.pair, 'histAmount': item.histAmount, 'amount': item.amount,'price': item.price, 'time': item.time, 'complete':item.complete, 'orderType': item.orderType}
	return JsonResponse(resJson)

def recentTrades(request):
	resJson = dict()
	for index, item in enumerate(TradeHistory.objects.filter(amount__gt=0).order_by('-time').iterator()):
		resJson[index] = {'type': item.type, 'pair': item.pair, 'pairPrice': item.price, 'amount': item.amount}
	return JsonResponse(resJson)


def echo(request):
	return render(request, 'exchange/echo.html')