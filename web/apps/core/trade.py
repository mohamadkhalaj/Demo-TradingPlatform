from django.conf import settings
from matplotlib.pyplot import hist
from .utils import calc_equivalent
from .models import Portfolio, TradeHistory


class Trade:
    def __init__(self, user, inputs):
        self.user = user
        self.portfo = Portfolio.objects.filter(usr=self.user, marketType='spot')
        self.orderType = inputs['orderType']
        self.type = inputs['type']
        self.pair = inputs['pair']
        self.base = inputs['pair'].split('-')[0]
        self.quote = inputs['pair'].split('-')[1]
        self.crp = inputs['amount'].split(' ')[1]
        self.amount = float(inputs['amount'].split(' ')[0])

    
    def spotTrade(self):
        message = None
        pairPrice = calc_equivalent(self.base, self.qoute)[0]

        if self.crp == self.base:
            equivalent = self.amount * pairPrice
            amount = f'{self.amount} {self.base}'

            if equivalent < settings.MINIMUM_TRADE_SIZE:
                message = f"minimum trade size is {settings.MINIMUM_TRADE_SIZE} $, but your's is:"\
                            +f"{self.amount} {self.crp}={round(equivalent, 2)}$ !"
            else:
                if self.type == 'buy':
                    is_available = self.check_available(equivalent, self.qoute)
                    toAdd = [self.base, self.amount]
                    toSub = [self.quote, equivalent]
                else:
                    is_available = self.check_available(self.amount, self.base)
                    toAdd = [self.quote, equivalent]
                    toSub = [self.base, self.amount]  

        else:
            equivalent = self.amount / pairPrice
            amount = f'{equivalent} {self.base}'

            if equivalent < settings.MINIMUM_TRADE_SIZE:
                message = f"minimum trade size is {settings.MINIMUM_TRADE_SIZE} $, but your's is:"\
                            +f"{self.amount} {self.crp}={self.amount}$ !"
            else:
                if self.type == 'buy':
                    is_available = self.check_available(self.amount, self.quote)
                    toAdd = [self.base, equivalent]
                    toSub = [self.quote, self.amount]
                else:
                    is_available = self.check_available(equivalent, self.base)
                    toAdd = [self.quote, self.amount]
                    toSub = [self.base, equivalent]

        if message:
            tradeResponse = {
                    "successful": False,
                    "message": message
            }
            return tradeResponse

        if is_available:
            obj = self.portfo.get(cryptoName=toSub[0])
            obj.amount = obj.amount - toSub[1]
            obj.save()

            obj, created = Portfolio.objects.get_or_create(
                usr=self.user,
                cryptoName=toAdd[0],
                amount=self.amount
            )

            if not created:
                obj.amount = obj.amount + toAdd[1]
                obj.save()

            histAmount = dict()
            for item in self.portfo.iterator():
                histAmount["cryptoName"] = item.cryptoName
                histAmount["amount"] = item.amount

            TradeHistory.objects.create(
                usr=self.user,
                type=self.type,
                pair=self.pair,
                histAmount=histAmount,
                amount=self.amount,
                price=pairPrice,
                complete=True,
                orderType=self.orderType,
                pairPrice=pairPrice
            )

            tradeResponse = {
                "successful": True,
                "message": 'Order filled!'
            }

            tradeResult = {
                "0": {
                    "type": self.type,
                    "pair": self.pair,
                    "pairPrice": pairPrice,
                    "amount": amount,
                }
            }

            executed_time = TradeHistory.objects.filter(usr=self.user).last().time.replace(tzinfo=None)

            return tradeResponse, tradeResult, executed_time

        else:
            tradeResponse = {
                "successful": False,
                "message": 'Insufficient balance!'
            }

        return tradeResponse


    def check_available(self, amount, name):
        try:
            obj = self.portfo.get(cryptoName=name)
            if amount <= obj.amount:
                return True
            else:
                return False
        except:
            return False   