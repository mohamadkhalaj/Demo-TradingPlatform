import time
from .common_functions import Give_equivalent
from .models import TradeHistory, Portfolio


class Trade:
    def __init__(self, type, pair, amount):
        self.result = None
        self.type = type
        self.pair = pair
        self.amount = amount
        self.base = pair.split('|')[0]
        self.qoute = pair.split('|')[1]
        self.pairPrice = 0
        self.equivalent = 0
        self.eq = Give_equivalent()
        self.funcs()

    def funcs(self):
        # get pair price and equivalent amount
        self.pairPrice, self.equivalent = self.eq.calc_equivalent(self.base, self.qoute, self.amount)
        # type = buy
        if self.type == 'buy':
            state = self.eq.check_available(self.equivalent, self.qoute)
            if state == 0:
                # subtract
                obj = Portfolio.objects.get(cryptoName=self.qoute)
                obj.amount = obj.amount - self.equivalent
                obj.save()
                # add
                try:
                    obj = Portfolio.objects.get(cryptoName=self.base)
                    obj.amount = obj.amount + self.amount
                    obj.save()
                except:
                    newCrypto = Portfolio(cryptoName=self.base, amount=self.amount,
                                          equivalentAmount=self.eq.calc_equivalent(self.base, 'USDT', self.amount)[1])
                    newCrypto.save()
        # type = sell
        else:
            state = self.eq.check_available(self.amount, self.base)
            if state == 0:
                # subtract
                obj = Portfolio.objects.get(cryptoName=self.base)
                obj.amount = obj.amount - self.amount
                obj.save()
                # add
                try:
                    obj = Portfolio.objects.get(cryptoName=self.qoute)
                    obj.amount = obj.amount + self.equivalent
                    obj.save()
                except:
                    newCrypto = Portfolio(cryptoName=self.qoute, amount=self.equivalent,
                                          equivalentAmount=self.eq.calc_equivalent(self.qoute, 'USDT', self.equivalent)[1])
                    newCrypto.save()
        # create history and give result
        if state == 0:
            newHistory = TradeHistory(type=self.type, pair=self.pair, pairPrice=self.pairPrice,
                                      amount=self.amount, price=self.equivalent, timeStamp=time.time())
            newHistory.save()
            self.result = {'state': 0, self.base: Portfolio.objects.get(cryptoName=self.base).amount,
                           self.qoute: Portfolio.objects.get(cryptoName=self.qoute).amount}
        else:
            self.result = {'state': state}
