from exchange.models import Portfolio, TradeHistory
from datetime import datetime, timedelta
import time
import requests
import matplotlib.pyplot as plt
import pandas as pd
import os


class Charts:
    def __init__(self, user):
        self.user = user
        self.portfo = Portfolio.objects.filter(usr=self.user)
        self.histories = TradeHistory.objects.filter(usr=self.user)
        self.dates = []
        self.values = []
        self.percents = []
        self.prices = dict()
        self.func()

    def func(self):
        os.mkdir('static\exchange\img\charts')

        all_start_date = self.histories.first().time.replace(tzinfo=None)
        now_timestamp = time.time()
        all_start_date = all_start_date + (datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp))
        end_date = datetime.now()

        daysAgo = (end_date - all_start_date).days
        if daysAgo >= 1:
            self.get_prices(daysAgo)
            self.pnl(all_start_date, end_date)
            if daysAgo > 30:
                self.dates = self.dates[-30:]
                self.values = self.values[-30:]
                self.percents = self.percents[-30:]
        else:
            self.dates.append(end_date.strftime('%m-%d'))
            self.get_latest()

        self.bar_chart(self.dates, self.values)

    def pnl(self, start_date, end_date):
        delta = timedelta(days=1)
        price_index = -1
        while start_date <= end_date:
            total = 0
            price_index += 1
            try:
                hst_dict = self.histories.filter(time__year=start_date.year, time__month=start_date.month,
                                                 time__day=start_date.day).last().histAmount
            except:
                pass
            for dc in hst_dict:
                crp = hst_dict[dc]['cryptoName']
                amount = float(hst_dict[dc]['amount'])
                total += self.prices[crp][price_index] * amount

            self.values.append(total - 1000)
            self.percents.append(round(((total - 1000) / 10), 2))
            self.dates.append(start_date.strftime('%m-%d'))

            start_date += delta

    def get_prices(self, limit):
        for index, item in enumerate(self.portfo.iterator()):
            self.prices[item.cryptoName] = []
            response = requests.get(
                'https://min-api.cryptocompare.com/data/v2/histoday?fsym='+item.cryptoName+'&tsym=USDT&limit='+str(limit))
            response = response.json()['Data']['Data']
            for i in response:
                self.prices[item.cryptoName].append(float(i['close']))

    def get_latest(self):
        total = 0
        for item in self.portfo.iterator():
            response = requests.get('https://min-api.cryptocompare.com/data/price?fsym='+item.cryptoName+'&tsyms=USDT')
            price = float(response.json()['USDT'])
            total += price * item.amount
        self.percents.append((total - 1000) / 10)
        self.values.append(total - 1000)

    def bar_chart(self, x, y):
        data = pd.DataFrame({'date': x, 'values': y, 'Percentage': self.percents})
        data['negative'] = data['values'] < 0
        plt.style.use('dark_background')
        plt.figure(figsize=(9, 7))
        graph = plt.bar(x, y, color=data.negative.map({True: 'r', False: 'g'}))

        i = 0
        for p in graph:
            width = p.get_width()
            height = p.get_height()
            x, y = p.get_xy()
            if height < 0:
                height -= 0.1
            plt.text(x + width / 2, height, str(self.percents[i]) + '%', ha='center', weight='bold')
            i += 1

        plt.axhline(y=0, color='white', linewidth=0.2)
        plt.xlabel('date')
        plt.ylabel('P&L amount (USDT)')
        plt.savefig('static\exchange\img\charts\pnl.png')
        plt.title('P&L chart')