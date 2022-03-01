from exchange.common_functions import calc_equivalent
from exchange.models import Portfolio, TradeHistory
from datetime import datetime, timedelta
from .models import User
import time, requests

class Charts:
    def __init__(self, user, portfo, histories):
        self.user = user
        self.portfo = portfo
        self.histories = histories
        self.dates = []
        self.values = []
        self.percents = []
        self.prices = dict()
        self.haveTrade = True
        self.func()

    def func(self):
        try:
            first_date = self.histories[0].time.replace(tzinfo=None)
            print(first_date)
        except Exception as e:
            print(e)
            self.haveTrade = False
            return
        now_timestamp = time.time()
        first_date = first_date + (datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp))
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)

        daysAgo = (end_date - first_date).days
        if daysAgo >= 1:
            self.get_prices((end_date - start_date).days)
            self.pnl(start_date, end_date)
        else:
            self.values = [0] * 30
            self.percents = [0] * 30
            delta = timedelta(days=1)
            while start_date <= end_date:
                self.dates.append(start_date.strftime('%m-%d'))
                start_date += delta
            self.get_latest()

    def pnl(self, start_date, end_date):
        delta = timedelta(days=1)
        price_index = -1
        hastrade = False
        while start_date <= end_date:
            total = 0
            price_index += 1
            try:
                hst_dict = self.histories.filter(time__year=start_date.year, time__month=start_date.month,
                                                 time__day=start_date.day).last().histAmount
                hastrade = True
            except:
                pass

            if hastrade:
                for dc in hst_dict:
                    crp = hst_dict[dc]['cryptoName']
                    amount = float(hst_dict[dc]['amount'])
                    total += self.prices[crp][price_index] * amount
                self.values.append(total - 1000)
                self.percents.append(round(((total - 1000) / 10), 2))
            else:
                self.values.append(0)
                self.percents.append(0)
            self.dates.append(start_date.strftime('%m-%d'))

            start_date += delta

    def get_prices(self, limit):
        for index, item in enumerate(self.portfo):
            self.prices[item.cryptoName] = []
            response = requests.get(
                'https://min-api.cryptocompare.com/data/v2/histoday?fsym='+item.cryptoName+'&tsym=USDT&limit='+str(limit))
            response = response.json()['Data']['Data']
            for i in response:
                self.prices[item.cryptoName].append(float(i['close']))

    def get_latest(self):
        total = 0
        for item in self.portfo:
            response = requests.get('https://min-api.cryptocompare.com/data/price?fsym='+item.cryptoName+'&tsyms=USDT')
            price = float(response.json()['USDT'])
            total += price * item.amount
        self.percents.append(round((total - 1000) / 10, 2))
        self.values.append(total - 1000)

    def bar_chart(self):
        if not self.haveTrade:
            return False
        x = self.dates 
        y = self.values
        return x, y

    def assetAllocation(self):
        cryptoDic = {}
        for index, item in enumerate(self.portfo):
            if calc_equivalent(item.cryptoName, 'USDT', item.amount)[1] != 0:
                cryptoDic[item.cryptoName] = calc_equivalent(
                                                    item.cryptoName, 
                                                    'USDT', 
                                                    item.amount)[1]
        
        labels = list(cryptoDic.keys())
        data = list(cryptoDic.values())

        assetAllocation = [['Asset', 'Percent']]
        for label, item in zip(labels, data):
            temp = []
            temp.append(label)
            temp.append(float(item))
            assetAllocation.append(temp)

        return assetAllocation