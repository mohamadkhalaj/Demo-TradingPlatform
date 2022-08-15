from datetime import datetime, timedelta

import requests
from django.conf import settings

from .utils import calc_equivalent


class Charts:
    def __init__(self, portfolio, histories):
        self.portfo = portfolio
        self.histories = histories
        self.dayNumber = 30

    def profit_loss(self):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=self.dayNumber)
        dates = [(start_date + timedelta(days=d)).strftime("%m-%d") for d in range(0, (end_date - start_date).days + 1)]

        if not self.histories:
            return dates, [0] * self.dayNumber

        first_date = self.histories[0].time.replace(tzinfo=None)
        prices = self.get_prices(self.dayNumber)
        daysAgo = (end_date - first_date).days

        if daysAgo < 1:
            baseBalance = settings.DEFAULT_BALANCE
            values = [0] * 29
            percents = [0] * 29
        else:
            if 1 <= daysAgo <= self.dayNumber:
                baseBalance = settings.DEFAULT_BALANCE
                historyDict = None
            else:
                historyDict, baseBalance = self.get_balance(None, start_date, prices, 0)

            values, percents = self.calculate_pnl(start_date, end_date, historyDict, prices, baseBalance)

        latestValue, latestPercentage = self.get_latest(baseBalance, prices)
        values.append(latestValue)
        percents.append(latestPercentage)

        return dates, values

    def get_latest(self, balance, prices):
        total = 0
        for item in self.portfo:
            price = prices[item.cryptoName][-1]
            total += price * item.amount

        value = total - balance
        percentage = round(value / 10, 2)

        return value, percentage

    def get_prices(self, limit):
        prices = dict()
        for item in self.portfo:
            response = requests.get(
                "https://min-api.cryptocompare.com/data/v2/histoday?fsym="
                + item.cryptoName
                + "&tsym=USDT&limit="
                + str(limit)
            )
            response = response.json()["Data"]["Data"]
            prices[item.cryptoName] = list()
            prices[item.cryptoName] = [float(resp["close"]) for resp in response]

        return prices

    def get_balance(self, historyDict, date, prices, price_index):
        if not historyDict:
            for hst in self.histories:
                curDate = hst.time.replace(tzinfo=None)
                if curDate < date:
                    historyDict = hst.histAmount

        total = 0
        for index in historyDict:
            crypto_name = historyDict[index]['cryptoName']
            amount = historyDict[index]['amount']
            total += prices[crypto_name][price_index] * amount

        return historyDict, total

    def calculate_pnl(self, start_date, end_date, historyDict, prices, baseBalance):
        values = []
        percents = []
        price_index = -1
        delta = timedelta(days=1)

        while start_date <= end_date:
            price_index += 1

            for item in self.histories:
                if (
                    item.time.year == start_date.year
                    and item.time.month == start_date.month
                    and item.time.day == start_date.day
                ):
                    historyDict = item.histAmount

            if historyDict:
                total = self.get_balance(historyDict, None, prices, price_index)[1]
            else:
                total = baseBalance

            sub = total - baseBalance
            values.append(sub)
            percents.append(sub / total * 100)

            start_date += delta

        return values, percents

    def asset_allocation(self):
        cryptoDic = {}
        for item in self.portfo:
            if calc_equivalent(item.cryptoName, "USDT", item.amount)[1] != 0:
                cryptoDic[item.cryptoName] = calc_equivalent(item.cryptoName, "USDT", item.amount)[1]

        labels = list(cryptoDic.keys())
        data = list(cryptoDic.values())

        assetAllocation = [["Asset", "Percent"]]
        for label, item in zip(labels, data):
            temp = []
            temp.append(label)
            temp.append(float(item))
            assetAllocation.append(temp)

        return assetAllocation
