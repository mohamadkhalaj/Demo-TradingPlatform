from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.layers import get_channel_layer
from core.trade import Trade
from core.utils import calc_equivalent, check_symbol_balance
from exchange.models import Portfolio, TradeHistory



class TradeConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.unicastName = f"{self.user}_unicast"

        if self.user.is_authenticated:
            await (self.channel_layer.group_add)(self.unicastName, self.channel_name)

        await self.accept()


    async def receive_json(self, content, **kwargs):
        result = await self.trade(content)
        print(result)
       
        try:
            tradeResponse, tradeResult, executedTime = result
        except ValueError:
            tradeResponse = result

        await self.channel_layer.group_send(self.unicastName, {"type": "send.data", "content": tradeResponse})
        

    async def send_data(self, event):
        data = event["content"]
        await self.send_json(data)
        
       
    @database_sync_to_async
    def trade(self, content):
        tradeObject = Trade(self.user, content)
        result = tradeObject.spotTrade()

        return result