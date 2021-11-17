import requests
from .models import Portfolio


class Give_equivalent:
    def calc_equivalent(self, base, qoute, amount):
        base = base.upper()
        response = requests.get("https://min-api.cryptocompare.com/data/pricemulti?fsyms=" + base + "," + qoute + "&tsyms=USDT,USDT")
        response = response.json()
        basePrice = float(response[base]['USDT'])
        qoutePrice = float(response[qoute]['USDT'])
        pairPrice = basePrice / qoutePrice
        equivalent = pairPrice * amount

        return pairPrice, equivalent

    def check_available(self, amount, name):
        try:
            obj = Portfolio.objects.get(cryptoName=name)
            if amount <= obj.amount:
                return 0
            else:
                return 1
        except:
            return 2