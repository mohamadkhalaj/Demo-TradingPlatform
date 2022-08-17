from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.layers import get_channel_layer
from django.db.models import F
from exchange.models import Portfolio

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
                {"type": "send.data", "content": await self.addOrder(content)},
            )
            await channel.group_send(
                f"{self.user}_ORDRunicast",
                {"type": "send.data", "content": self.limit_order},
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

        if amount.split(" ")[1] == pair.split("-")[0]:
            famount = amount
        else:
            famount = f"{float(amount.split(' ')[1]) / float(targetPrice)} {pair.split('-')[0]}"

        obj = LimitOrders.objects.create(
            usr=self.user,
            type=content["type"],
            pair=pair,
            amount=famount,
            pairPrice=targetPrice,
            amount_float=float(famount.split()[0]),
        )
        if content["type"] == "buy":
            obj.equivalentAmount = F("amount_float") * F("pairPrice")
            obj.save()
        type_ = 1 if content["type"] == "buy" else 0
        p_price = targetPrice * float(famount.split()[0]) if content["type"] == "buy" else float(famount.split()[0])
        Portfolio.objects.filter(usr=self.user, cryptoName=pair.split("-")[type_]).update(amount=F("amount") - p_price)

        executed_time = LimitOrders.objects.filter(usr=self.user).last().time.replace(tzinfo=None)
        newId = LimitOrders.objects.filter(usr=self.user).last().id
        result = {
            "0": {
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
        self.limit_order = result
        return result

    @database_sync_to_async
    def cancelOrder(self, ids):
        orders = LimitOrders.objects.filter(
            usr=self.user,
            pk__in=ids,
        )
        for order in orders:
            type_ = 1 if order.type == "buy" else 0
            p_price = order.pairPrice * order.amount_float if order.type == "buy" else order.amount_float
            Portfolio.objects.filter(usr=self.user, cryptoName=order.pair.split("-")[type_]).update(
                amount=F("amount") + p_price
            )
        orders.delete()
