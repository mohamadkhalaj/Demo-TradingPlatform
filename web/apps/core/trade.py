from django.conf import settings
from exchange.models import Portfolio, TradeHistory
from .utils import calc_equivalent


class Trade:
    def __init__(self, user, inputs):
        self.user = user
        self.portfo = Portfolio.objects.filter(usr=self.user, marketType="spot")
        self.orderType = inputs["orderType"]
        self.type = inputs["type"]
        self.pair = inputs["pair"]
        self.base = inputs["pair"].split("-")[0]
        self.quote = inputs["pair"].split("-")[1]
        self.crp = inputs["amount"].split(" ")[1]
        self.amount = float(inputs["amount"].split(" ")[0])

    def spotTrade(self):
        message = None
        pairPrice = calc_equivalent(self.base, self.quote)

        if self.crp == self.base:
            equivalent = self.amount * pairPrice
            amount = f"{self.amount} {self.base}"

            if equivalent < settings.MINIMUM_TRADE_SIZE:
                message = (
                    f"minimum trade size is {settings.MINIMUM_TRADE_SIZE} $, but your's is: "
                    + f"{self.amount} {self.crp}={round(equivalent, 2)}$ !"
                )
            else:
                if self.type == "buy":
                    is_available = self.check_available(equivalent, self.quote)
                    toAdd = [self.base, self.amount]
                    toSub = [self.quote, equivalent]
                else:
                    is_available = self.check_available(self.amount, self.base)
                    toAdd = [self.quote, equivalent]
                    toSub = [self.base, self.amount]

        else:
            equivalent = self.amount / pairPrice
            amount = f"{equivalent} {self.base}"

            if self.amount < settings.MINIMUM_TRADE_SIZE:
                message = f"minimum trade size is {settings.MINIMUM_TRADE_SIZE} $, but your's is: {self.amount} $ !"
            else:
                if self.type == "buy":
                    is_available = self.check_available(self.amount, self.quote)
                    toAdd = [self.base, equivalent]
                    toSub = [self.quote, self.amount]
                else:
                    is_available = self.check_available(equivalent, self.base)
                    toAdd = [self.quote, self.amount]
                    toSub = [self.base, equivalent]

        if message:
            tradeResponse = {"successful": False, "message": message}
            return tradeResponse

        if is_available:
            updatedAsset = dict()

            obj = self.portfo.get(cryptoName=toSub[0])
            obj.amount = obj.amount - toSub[1]
            obj.save()
            updatedAsset["0"] = {
                "cryptoName": toSub[0],
                "amount": obj.amount,
                "equivalentAmount": obj.get_dollar_equivalent,
            }

            try:
                obj = self.portfo.get(cryptoName=toAdd[0])
                obj.amount = obj.amount + toAdd[1]
                obj.save()
            except:
                obj = Portfolio(usr=self.user, cryptoName=toAdd[0], amount=toAdd[1])
                obj.save()
            updatedAsset["1"] = {
                "cryptoName": toAdd[0],
                "amount": obj.amount,
                "equivalentAmount": obj.get_dollar_equivalent,
            }
                

            histAmount = dict()
            for item in self.portfo.iterator():
                histAmount[item.cryptoName] = item.amount

            TradeHistory.objects.create(
                usr=self.user,
                type=self.type,
                pair=self.pair,
                histAmount=histAmount,
                amount=amount,
                complete=True,
                orderType=self.orderType,
                pairPrice=pairPrice,
            )

            tradeResponse = {"successful": True, "message": "Order filled!"}

            executed_time = TradeHistory.objects.filter(usr=self.user).last().time
            tradeResult = {
                "0": {
                    "type": self.type,
                    "pair": self.pair,
                    "pairPrice": pairPrice,
                    "amount": amount,
                    "time": executed_time.timestamp(),
                    "orderType": "market",
                    "complete": True,
                    "newHistory": True,
                }
            }

            return tradeResponse, tradeResult, updatedAsset

        else:
            tradeResponse = {"successful": False, "message": "Insufficient balance!"}

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