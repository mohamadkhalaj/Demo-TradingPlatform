import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer

class OrdersConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.group_name = 'bookOrder'
        await self.accept()
        await (self.channel_layer.group_add)(self.group_name, self.channel_name)
        # await (self.channel_layer.group_send)(
        #     'bookOrder',
		#     {
        #         'type': 'order.display',
        #         'content': 'valueee'
		#     }
        # )
        

    async def receive_json(self, content, **kwargs):
        print('here at receive method')

    async def disconnect(self, code):
        await (self.channel_layer.group_discard)(self.group_name, self.channel_name)

    async def order_display(self, event):
        print('here at function')
        data = event['content']
        await self.send_json(data)