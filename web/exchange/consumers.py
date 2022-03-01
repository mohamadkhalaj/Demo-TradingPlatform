from turtle import st
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from .trade import Trade
import re
import json
from channels.db import database_sync_to_async

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
 
        await self.accept()


    async def receive_json(self, content, **kwargs):
        print(content)
        self.header = content['header']
        self.orderType = content['orderType']

        result = await self.trade(content)
        print(result)
        trade_response = {'header': 'trade_response', 'state': result['state']}
        
        await self.channel_layer.group_send(
			self.unicastName,
			{
				'type': 'send.data',
				'content': trade_response
			}
		)
        
    async def disconnect(self, code):
        pass


    @database_sync_to_async
    def trade(self, content):
        if self.header == 'trade_request' and self.orderType == 'market':
            tradeObject = Trade(self.user, self.orderType, content['type'], content['pair'], content['amount'])
            result = tradeObject.result

            return result


    async def send_data(self, event):
        data = event['content']
        await self.send_json(data)
            