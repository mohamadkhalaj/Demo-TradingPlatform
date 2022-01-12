from exchange.common_functions import calc_equivalent
from exchange.models import Portfolio, TradeHistory
from datetime import datetime, timedelta
import os, uuid, time, requests, random
import matplotlib.pyplot as plt
from .models import User
import pandas as pd

class Charts:
    def __init__(self, user):
        self.user = user
        self.portfo = Portfolio.objects.filter(usr=self.user)
        self.histories = TradeHistory.objects.filter(usr=self.user)
        self.dates = []
        self.values = []
        self.percents = []
        self.prices = dict()
        self.haveTrade = True
        self.func()

    def func(self):
        if not os.path.exists('static/exchange/img/charts'):
            os.mkdir('static/exchange/img/charts')

        try:
            first_date = self.histories.first().time.replace(tzinfo=None)
        except:
            self.haveTrade = False
            print('This user has\'nt any trade.')
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

    def assetAllocation(self):
        cryptoDic = {}
        totalCR = []
        for index, item in enumerate(self.portfo):
            if calc_equivalent(item.cryptoName, 'USDT', item.amount)[1] != 0:
                cryptoDic[item.cryptoName] = calc_equivalent(item.cryptoName, 'USDT', item.amount)[1]
        
        labels = list(cryptoDic.keys())
        fig, ax = plt.subplots(figsize=(6,4))
        ax.figure.set_facecolor('#121212')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        patches, texts, autotexts = ax.pie(list(cryptoDic.values()),labels = labels ,autopct='%1.1f%%', pctdistance=0.8)
        [text.set_color('white') for text in texts]
        my_circle = plt.Circle((0, 0), 0.45, color='#1e222d')
        plt.gca().add_artist(my_circle)
        uId = uuid.uuid4().hex[:25].upper()
        obj = User.objects.get(username=self.user)

        if obj.assetUUID != '0':
            try:
                os.remove('static/exchange/img/charts/asset' + obj.assetUUID + '.png')
            except:
                pass

        obj.assetUUID = uId
        obj.save()
        fileName = 'asset' + uId + '.png'
        plt.savefig('static/exchange/img/charts/' + fileName, transparent=True)

        return fileName

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
        self.percents.append(round((total - 1000) / 10, 2))
        self.values.append(total - 1000)

    def bar_chart(self):
        if not self.haveTrade:
            return False
        x = self.dates 
        y = self.values
        data = pd.DataFrame({'date': x, 'values': y, 'Percentage': self.percents})
        data['negative'] = data['values'] < 0
        plt.figure(figsize=(11, 6))
        graph = plt.bar(x, [value/10 for value in self.values], color=data.negative.map({True: 'r', False: 'g'}), width = 0.6)

        i = 0
        axes = plt.gca()
        di = max(axes.get_ylim())/100
        diTemp = abs(di)
        for p in graph:
            width = p.get_width()
            height = p.get_height()
            x, y = p.get_xy()
            barTextHeight = int()
            if height < 0:
                barTextHeight = - random.uniform(diTemp * 30, diTemp * 45) 
                height -= di
            else:
                barTextHeight = random.uniform(diTemp * 30, diTemp * 45)
                height += di
            if self.percents[i]:

                plt.text(x + width / 2, height + barTextHeight, str(round(self.percents[i], 1)) + '%', ha='center', color='white', size=6)
            i += 1

        plt.axhline(y=0, color='white', linewidth=0.2)
        plt.xlabel('date', color='white')
        plt.ylabel('PNL Percentage(%)', color='white')
        plt.tick_params(axis='x', colors='white')
        plt.tick_params(axis='y', colors='white')
        uId = uuid.uuid4().hex[:25].upper()
        obj = User.objects.get(username=self.user)
        if obj.pnlUUID != '0':
            try:
                os.remove('static/exchange/img/charts/pnl' + obj.pnlUUID + '.png')
            except:
                pass
        obj.pnlUUID = uId
        obj.save()
        fileName = 'pnl' + uId + '.png'
        plt.xticks(rotation=45, fontsize=7)
        plt.tick_params(axis='x', colors='white')
        plt.tick_params(axis='y', colors='white')
        axes.spines['right'].set_color('none')
        axes.spines['top'].set_color('none')
        plt.savefig('static/exchange/img/charts/' + fileName, transparent=True)

        return fileName