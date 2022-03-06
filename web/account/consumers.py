from channels.generic.websocket import AsyncJsonWebsocketConsumer
from exchange.common_functions import calc_equivalent, pretify
from exchange.models import Portfolio, TradeHistory
from channels.db import database_sync_to_async
import asyncio, cryptocompare, requests, json
from decouple import config
from .charts import Charts

def getCryptoList(page, limit):
    url = f'https://min-api.cryptocompare.com/data/top/mktcap?limit={limit}&tsym=USD&page={page}'

    cryptos = requests.get(url).json()['Data']
    dictionary = {}
    for index, crypto in enumerate(cryptos):
        cr = crypto['CoinInfo']
        dictionary[cr['Name']] = cr['FullName']
        dictionary[cr['Name'] + '_rank'] = (page * limit) + (index + 1)
    return dictionary

def cryptoJson(data):
    global dictionary
    data = data['DISPLAY']

    domain = 'https://cryptocompare.com'
    array = []
    for item in data:
        tmp = data[item]["USD"]
        array.append(
                {
                    "symbol": item,
                    "name": dictionary.get(item, ''),
                    "rank": dictionary.get(item + '_rank', ''),
                    "price": tmp["PRICE"].strip('$ '),
                    "24c": tmp["CHANGEPCT24HOUR"],
                    "mc": tmp["MKTCAP"].strip('$ '),
                    "24h": tmp["HIGH24HOUR"].strip('$ '),
                    "24l": tmp["LOW24HOUR"].strip('$ '),
                    "vol": tmp["VOLUME24HOURTO"].strip('$ '),
                    "img": domain + tmp["IMAGEURL"],
                }
            )
    return array

class MarketConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def sendList(self, subs):

        CRYPTO_COMPARE_API = config('CRYPTO_COMPARE_API')
        cryptocompare.cryptocompare._set_api_key_parameter(CRYPTO_COMPARE_API)  

        data = cryptocompare.get_price(subs, currency='USD', full=True)
        # print(cryptoJson(data))
        await self.send_json(cryptoJson(data))
        await asyncio.sleep(1)

    async def disconnect(self, close_code):
        self.close()

    async def receive(self, text_data=None, bytes_data=None):
        global dictionary
        if text_data:
            page = json.loads(text_data)['page']
            dictionary = getCryptoList(page, 20)
            temp = list(dictionary.keys())
            subs = []
            for item in temp:
                if '_rank' not in item:
                    subs.append(item)
            while True:
                await asyncio.ensure_future(self.sendList(subs))


class ChartSocket(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_authenticated:
            await self.accept()
        else:
            self.close()

    async def sendData(self):
        portfolio = await self.getPortfolio()
        trades = await self.getTrades()

        dictionary = {}

        chart = Charts(self.user, portfolio, trades)
        assetAllocation = chart.assetAllocation()
        pnl = chart.bar_chart()

        dictionary['assetAllocation'] = assetAllocation
        dictionary['pnl'] = pnl

        await self.send_json(dictionary)
        await asyncio.sleep(60)

    async def disconnect(self, close_code):
        self.close()

    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            while True:
                await asyncio.ensure_future(self.sendData())

    @database_sync_to_async
    def getPortfolio(self):
        return list(Portfolio.objects.all().filter(
                usr=self.user, 
                marketType='spot', 
            )
        )

    @database_sync_to_async
    def getTrades(self):
        return list(TradeHistory.objects.all().filter(
                usr=self.user, 
                complete=True,
            )
        )


class WalletSocket(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_authenticated:
            await self.accept()
        else:
            self.close()

    async def sendData(self):
        domain = 'https://cryptocompare.com'

        CRYPTO_COMPARE_API = config('CRYPTO_COMPARE_API')
        cryptocompare.cryptocompare._set_api_key_parameter(CRYPTO_COMPARE_API)  
        portfolio = await self.getPortfolio()
        dictionary = {}
        totalMargin = pretify(
            sum(
                    [calc_equivalent(
                        item.cryptoName, 
                        'USDT', 
                        item.amount)[1] for item in portfolio]
                )
            )
        
        assets = {}
        for item in portfolio:
            assets[item.cryptoName] = float(item.amount)

        array = []
        data = cryptocompare.get_price(
                list(assets.keys()), 
                currency='USD', 
                full=True
            )['RAW']

        for item in data:
            tmp = data[item]["USD"]
            price = float(tmp["PRICE"])
            total = price * assets[item]
            array.append(
                    {
                        "symbol": item,
                        "amount": assets[item],
                        "total" : total,
                        "img": domain + tmp["IMAGEURL"],
                    }
                )

        dictionary['total'] = totalMargin
        dictionary['assets'] = array

        await self.send_json(dictionary)
        await asyncio.sleep(1)

    async def disconnect(self, close_code):
        self.close()

    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            while True:
                await asyncio.ensure_future(self.sendData())

    @database_sync_to_async
    def getPortfolio(self):
        return list(Portfolio.objects.all().filter(
                usr=self.user, 
                marketType='spot', 
                amount__gt=0,
            )
        )