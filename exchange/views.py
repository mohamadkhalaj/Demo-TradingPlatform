from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import get_user_model
from .common_functions import Give_equivalent, pretify
from .models import TradeHistory, Portfolio
from django.core.paginator import Paginator
from django.shortcuts import render
from .trade import Trade
import json, re, requests


def home(request):
	return render(request, 'exchange/index.html')


def signUp(request):
	return render(request, 'registration/signup.html')

def markets(request, page=1):
	url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=USD&order=market_cap_desc&per_page=250&page=1&sparkline=false'
	data = requests.get(url).json()

	url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=USD&order=market_cap_desc&per_page=250&page=2&sparkline=false'
	data.extend(requests.get(url).json())

	paginator = Paginator(data, 50)
	data = paginator.get_page(page)

	for item in data:
		item['current_price'] = pretify(item['current_price'])
		item['market_cap'] = pretify(item['market_cap'])

		try:
			item['price_change_percentage_24h'] = float(pretify(item['price_change_percentage_24h']))
		except:
			item['price_change_percentage_24h'] = pretify(item['price_change_percentage_24h'])

		item['high_24h'] = pretify(item['high_24h'])
		item['low_24h'] = pretify(item['low_24h'])
		item['total_volume'] = pretify(item['total_volume'])

	context = {'data': data}

	return render(request, 'exchange/markets.html', context=context)

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
	for index, item in enumerate(TradeHistory.objects.filter(usr=request.user, amount__gt=0).order_by('-time').iterator()):
		resJson[index] = {'type': item.type, 'pair': item.pair, 'pairPrice': item.pairPrice, 'amount': item.amount,'price': item.price, 'time': item.time}
	return JsonResponse(resJson)
