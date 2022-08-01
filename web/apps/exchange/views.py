import json
import urllib.parse

import requests
from core.utils import search_symbol
from django.http import JsonResponse
from django.shortcuts import redirect, render
from requests.structures import CaseInsensitiveDict


def exchange_trade(request, pair="BINANCE:BTCUSDT"):

    if pair != "BINANCE:BTCUSDT":
        name = pair.split("-")[0]
        pair = search_symbol(pair)
    else:
        name = "BTC"

    context = {"pair": pair, "name": name.upper()}

    if not pair:
        pair = "BINANCE:BTCUSDT"
        name = "BTC"

        context = {
            "pair": pair,
            "name": name.upper(),
        }
        return redirect("/account/trade/BTC-USDT")
    else:
        return render(request, "registration/trade.html", context=context)


def search_cryptos(request, value):

    headers = CaseInsensitiveDict()
    url = "https://arzdigital.com/wp-admin/admin-ajax.php"
    headers["Content-Type"] = "application/x-www-form-urlencoded"

    encoddedValue = urllib.parse.quote_plus(json.dumps({"s": value}))
    data = f"action=arzAjax&query=search&data={encoddedValue}"

    try:
        resp = requests.post(url, headers=headers, data=data).json().get("coins", "null")
    except:
        resp = "null"

    if resp != "null":
        for item in resp:
            item["image"] = f'https://cdn.arzdigital.com/uploads/assets/coins/icons/32x32/{item["slug"]}.png'
    return JsonResponse(resp, safe=False)


def markets(request):
    return render(request, "exchange/markets.html")
