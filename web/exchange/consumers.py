from turtle import st
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from exchange.common_functions import calc_equivalent, pretify, search
from .trade import Trade
from .models import TradeHistory
import re
import json, asyncio, requests, cryptocompare
from channels.db import database_sync_to_async
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
        print('content:', content)
        self.header = content['header']
        self.orderType = content['orderType']
        self.pair = content['pair']
        result = await self.trade(content)
        print('result: ', result)
        # subs = getCryptoList(1,20)

        trade_response = {'header': 'trade_response', 'state': result['state']}
        hist_response = {'header': 'hist_response', 'type': result['type'], 'pair': self.pair, 'amount': result['amount'],'price': result['price'], 'time': result['time'], 'orderType': self.orderType}
        recentTrades_response = {'header': 'recent_response', 'type': result['type'], 'pair': self.pair, 'pairPrice': result['price'], 'amount': result['amount']}

        # await self.channel_layer.group_send(
		# 	self.broadcastName,
		# 	{
		# 		'type': 'send.data',
		# 		'content': price_response
		# 	}
		# )
        await self.channel_layer.group_send(
            self.unicastName,
            {
                'type': 'send.data',
                'content': trade_response
            }
        )

        if result['state'] == 0:
            await self.channel_layer.group_send(
                self.unicastName,
                {
                    'type': 'send.data',
                    'content': hist_response
                }
            )

            await self.channel_layer.group_send(
                self.broadcastName,
                {
                    'type': 'send.data',
                    'content': recentTrades_response
                }
            )
        # while True:
        #     price_response = await asyncio.ensure_future(self.sendList(subs))
            
        #     await self.channel_layer.group_send(
        #         self.broadcastName,
        #         {
        #             'type': 'send.data',
        #             'content': price_response
        #         }
        #     )
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



    def getCryptoList(page, limit):
        url = f'https://min-api.cryptocompare.com/data/top/mktcap?limit={limit}&tsym=USD&page={page}'

        cryptos = requests.get(url).json()['Data']
        dictionary = {}
        for index, crypto in enumerate(cryptos):
            cr = crypto['CoinInfo']
            dictionary[cr['Name']] = cr['FullName']
            dictionary[cr['Name'] + '_rank'] = (page * limit) + (index + 1)
        temp = list(dictionary.keys())
        subs = []
        for item in temp:
            if '_rank' not in item:
                subs.append(item)
        return(subs)

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

    def sendList(self, subs):

        CRYPTO_COMPARE_API = config('CRYPTO_COMPARE_API')
        cryptocompare.cryptocompare._set_api_key_parameter(CRYPTO_COMPARE_API)  

        data = cryptocompare.get_price(subs, currency='USD', full=True)

        print(cryptoJson(data))
        self.sleep(1)
        return(cryptoJson(data))
# def price(self, pair='BINANCE:BTCUSDT'):
# 	url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=USD&order=market_cap_desc&per_page=20&page=1&sparkline=false'
# 	data = requests.get(url).json()

# 	for item in data:
# 		item['current_price'] = pretify(item['current_price'])

# 		try:
# 			item['price_change_percentage_24h'] = float(pretify(item['price_change_percentage_24h']))
# 		except:
# 			item['price_change_percentage_24h'] = pretify(item['price_change_percentage_24h'])
	
# 	if pair != 'BINANCE:BTCUSDT':
# 		name = pair.split('-')[0]
# 		pair = search(pair)
# 	else:
# 		name = 'BTC'

# 	context = {
# 		'pair' : pair,
# 		'name' : name.upper(),
# 		'data' : data,
# 	}
# 	if not pair:
# 		pair = 'BINANCE:BTCUSDT'
# 		name = 'BTC'

# 		context = {
# 			'pair' : pair,
# 			'name' : name.upper(),
# 		}
# 		return ('/account/trade/BTC-USDT')
# 	else:
# 		return context
