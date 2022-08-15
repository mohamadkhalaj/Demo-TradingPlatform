from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.layers import get_channel_layer
from .models import LimitOrders


class LimitConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"] 
        await self.accept()


    async def receive_json(self, content, **kwargs):
        if content.get("pair"):       
            channel = get_channel_layer()
            await channel.group_send(
                f"{self.user}_histories", 
                {"type": "send.data", "content": await self.addOrder(content)}
            )
        else:
            await self.cancelOrder(content.get("cancel"))
           

    async def disconnect(self, code):
        self.close()


    async def send_data(self, event):
       pass
        
       
    @database_sync_to_async
    def addOrder(self, content):
        amount = content["amount"]
        targetPrice = content["targetPrice"]
        pair = content["pair"]

        if amount.split(' ')[1] == pair.split('-')[0]:
            famount = amount
        else:
            famount = f"{float(amount.split(' ')[1]) / float(targetPrice)} {pair.split('-')[0]}"

        LimitOrders.objects.create(
            usr=self.user,
            type=content["type"],
            pair=pair,
            amount=famount,
            pairPrice=targetPrice,
        )

        executed_time = LimitOrders.objects.filter(usr=self.user).last().time.replace(tzinfo=None)
        newId = LimitOrders.objects.filter(usr=self.user).last().id
        result = {
            "0":{
                "id": newId,
                "type": content["type"],
                "pair": content["pair"],
                "pairPrice": targetPrice,
                "amount": famount,
                "datetime": executed_time.strftime("%Y/%m/%d %H:%M"),
                "orderType": "limit",
                "complete": False,
            }
        }

        return result


    @database_sync_to_async
    def cancelOrder(self, ids):
        LimitOrders.objects.filter(
            usr=self.user,
            pk__in=ids,
        ).delete()