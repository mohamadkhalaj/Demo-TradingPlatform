import asyncio
import json

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from core.utils import create_crypto_json, get_crypto_compare, get_crypto_list
from exchange.models import Portfolio


class MarketConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def sendList(self, subs):

        cryptocompare = get_crypto_compare()
        data = cryptocompare.get_price(subs, currency="USD", full=True)
        await self.send_json(create_crypto_json(data, self.request_type, self.dictionary))
        await asyncio.sleep(1)

    async def disconnect(self, close_code):
        self.close()

    async def receive(self, text_data=None, bytes_data=None):

        self.request_type = json.loads(text_data)["RequestType"]
        if text_data:
            page = json.loads(text_data)["page"]
            self.dictionary = get_crypto_list(page, 20)
            temp = list(self.dictionary.keys())
            subs = []
            for item in temp:
                if "_rank" not in item:
                    subs.append(item)
            while True:
                await asyncio.ensure_future(self.sendList(subs))

   
    
class AssetConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.unicastName = f"{self.user}_asset"

        if self.user.is_authenticated:
            await (self.channel_layer.group_add)(self.unicastName, self.channel_name)

        await self.accept()


    async def receive_json(self, content, **kwargs):
        currentPair = content.get("currentPair")
        await self.send_json(await self.get_assetAmount(currentPair))


    async def disconnect(self, code):
        self.channel_layer.group_discard("unicastName", self.channel_name)
        self.close()


    async def send_data(self, event):
        data = event["content"]
        await self.send_json(data)


    @database_sync_to_async
    def get_assetAmount(self, pair):
        result = dict()
        
        for index, currency in enumerate([pair.split('-')[0], pair.split('-')[1]]):
            try:
                portfo = Portfolio.objects.get(cryptoName=currency, usr=self.user)       
                equivalentAmount = portfo.get_dollar_equivalent if currency != 'USDT' else None
                amount = portfo.amount
            except Portfolio.DoesNotExist:
                amount = 0
                equivalentAmount = 0

            result[str(index)] = {
                    "cryptoName": currency,
                    "amount": amount,
                    "equivalentAmount": equivalentAmount,
                }

        return result