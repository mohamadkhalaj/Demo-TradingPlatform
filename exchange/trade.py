from .models import TradeHistory, Portfolio
import requests


class Trade:
    def __init__(self, user, type, pair, amount):
        self.user = user
        self.portfo = Portfolio.objects.filter(usr=self.user)
        self.result = None
        self.type = type
        self.pair = pair
        self.amount = amount
        self.base = pair.split('|')[0]
        self.qoute = pair.split('|')[1]
        self.pairPrice = 0
        self.equivalent = 0
        self.callf()
        # dict = {'pair':'ETH|USDT', 'type':'buy', 'amount':'0.02'}

    def callf(self):
        self.pairPrice, self.equivalent = self.calc_equivalent(self.base, self.qoute, self.amount)
        # type = buy
        if self.type == 'buy':
            state = self.check_available(self.equivalent, self.qoute)
            if state == 0:
                # subtract
                obj = self.portfo.get(cryptoName=self.qoute)
                obj.amount = obj.amount - self.equivalent
                obj.save()
                # add
                try:
                    obj = self.portfo.get(cryptoName=self.base)
                    obj.amount = obj.amount + self.amount
                    obj.save()
                except:
                    newCrypto = Portfolio(usr=self.user, cryptoName=self.base, amount=self.amount,
                                          equivalentAmount=self.calc_equivalent(self.base, 'USDT', self.amount)[1])
                    newCrypto.save()
        # type = sell
        else:
            state = self.check_available(self.amount, self.base)
            if state == 0:
                # subtract
                obj = self.portfo.get(cryptoName=self.base)
                obj.amount = obj.amount - self.amount
                obj.save()
                # add
                try:
                    obj = self.portfo.get(cryptoName=self.qoute)
                    obj.amount = obj.amount + self.equivalent
                    obj.save()
                except:
                    newCrypto = Portfolio(usr=self.user, cryptoName=self.qoute, amount=self.equivalent,
                                          equivalentAmount=self.calc_equivalent(self.qoute, 'USDT', self.equivalent)[1])
                    newCrypto.save()
        # create history and give results
        if state == 0:
            newHistory = TradeHistory(usr=self.user, type=self.type, pair=self.pair, pairPrice=self.pairPrice,
                                      amount=self.amount, price=self.equivalent)
            newHistory.save()
            self.result = {'state': 0, self.base: self.portfo.get(cryptoName=self.base).amount,
                           self.qoute: self.portfo.get(cryptoName=self.qoute).amount}
        else:
            self.result = {'state': state}

    def calc_equivalent(self, base, qoute, amount):
        base = base.upper()
        response = requests.get(
            "https://min-api.cryptocompare.com/data/pricemulti?fsyms=" + base + "," + qoute + "&tsyms=USDT,USDT")
        response = response.json()
        basePrice = float(response[base]['USDT'])
        qoutePrice = float(response[qoute]['USDT'])
        pairPrice = basePrice / qoutePrice
        equivalent = pairPrice * amount

        return pairPrice, equivalent

    def check_available(self, amount, name):
        try:
            obj = self.portfo.get(cryptoName=name)
            if amount <= obj.amount:
                return 0
            else:
                return 1
        except:
            return 2