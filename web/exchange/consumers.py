from turtle import st
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from exchange.common_functions import calc_equivalent, pretify, search
from .trade import Trade
from .models import TradeHistory
import re
import json, asyncio, requests, cryptocompare
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
from decouple import config

# class OrdersConsumer(AsyncJsonWebsocketConsumer):
#     async def connect(self):
#         self.group_name = 'orderBook'
#         await self.accept()
#         await (self.channel_layer.group_add)(self.group_name, self.channel_name)


#     async def receive_json(self, content, **kwargs):
#         print('here at receive method')


#     async def disconnect(self, code):
#         await (self.channel_layer.group_discard)(self.group_name, self.channel_name)


#     async def order_display(self, event):
#         data = event['content']
#         await self.send_json(data)
# ##################################
class TradeConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.broadcastName = 'broadcast'
        self.unicastName= f'{self.user}_unicast'

        if self.user.is_authenticated:
            await (self.channel_layer.group_add)(
                self.unicastName,
                self.channel_name
            )

        await (self.channel_layer.group_add)(
            self.broadcastName,
            self.channel_name
        )

        
        await self.accept()


    async def receive_json(self, content, **kwargs):
        # print('content:', content)
        self.header = content['header']

        if self.header == 'current_pair':
            self.current_pair = content['current_pair']
            await self.initialFillings()

        elif self.header == 'trade_request':
            self.pair = content['pair']
            self.orderType = content['orderType']
            result = await self.trade(content)
            # print('result: ', result)
            trade_response = {'header': 'trade_response', 'state': result['state']}
            await self.channel_layer.group_send(
            self.unicastName,
                {
                    'type': 'send.data',
                    'content': trade_response
                }
            )
            if result['state'] == 0:
                hist_response = {'header': 'hist_response', 'type': result['type'], 'pair': self.pair, 'amount': result['amount'],'price': result['price'], 'orderType': self.orderType, 'date': result['date'], 'famount': result['famount'], 'pairPrice': result['pairPrice']}
                await self.channel_layer.group_send(
                    self.unicastName,
                    {
                        'type': 'send.data',
                        'content': hist_response
                    }
                )
                recentTrades_response = {'header': 'recent_response', 'type': result['type'], 'pair': result['pair'], 'price': result['pairPrice'], 'amount': result['famount'], 'time': result['time']}
                await self.channel_layer.group_send(
                    self.broadcastName,
                    {
                        'type': 'send.data',
                        'content': recentTrades_response
                    }
                )
    async def disconnect(self, code):
        self.channel_layer.group_discard

    
    async def send_data(self, event):
        data = event['content']
        print('data:', data)
        await self.send_json(data)

    @database_sync_to_async
    def trade(self, content):
        if self.header == 'trade_request' and self.orderType == 'market':
            tradeObject = Trade(self.user, self.orderType, content['type'], content['pair'], content['amount'])
            result = tradeObject.result

            return result

    @database_sync_to_async
    def initialFillings(self):
        histObj = TradeHistory.objects.all().order_by('-time')
        counter = 0
        for item in histObj.iterator():
            pair = item.pair.replace('-', '').upper()
            hist_content = {'header': 'hist_response', 'type': item.type, 'pair': item.pair, 'pairPrice': item.pairPrice, 'famount': item.amount, 'date': item.time.strftime("%Y:%m:%d:%H:%M"), 'price': item.price}          
            async_to_sync (self.channel_layer.group_send)(
                self.unicastName,
                {
                    'type': 'send.data',
                    'content': hist_content
                }
            )
            if pair == self.current_pair and counter <= 5:
                recent_content = {'header': 'recent_response', 'type': item.type, 'pair': pair, 'price': item.pairPrice, 'amount': item.amount, 'time': item.time.strftime("%H:%M:%S")}
                async_to_sync (self.channel_layer.group_send)(
                    self.unicastName,
                    {
                        'type': 'send.data',
                        'content': recent_content
                    }
                )
            counter += 1
        
# ##########################################################################3


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
                    "pair": item + '-USDT'
                }
            )
    return array

class PriceConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.broadcastName = 'broadcast'
        await (self.channel_layer.group_add)(
            self.broadcastName,
            self.channel_name
        )
        await self.accept()
    async def sendList(self, subs):

        CRYPTO_COMPARE_API = config('CRYPTO_COMPARE_API')
        cryptocompare.cryptocompare._set_api_key_parameter(CRYPTO_COMPARE_API)  

        data = cryptocompare.get_price(subs, currency='USD', full=True)

        await asyncio.sleep(1)
        return cryptoJson(data)

    async def disconnect(self, close_code):
        self.close()

    async def receive(self, text_data=None, bytes_data=None):
        global dictionary
        print('hello')
        if text_data:
            dictionary = getCryptoList(0, 20)
            temp = list(dictionary.keys())
            subs = []
            for item in temp:
                if '_rank' not in item:
                    subs.append(item)
            while True:
                price_response = await asyncio.ensure_future(self.sendList(subs))
                
                await self.channel_layer.group_send(
                    self.broadcastName,
                    {
                        'type': 'send.data',
                        'content': price_response
                    }
                )
                