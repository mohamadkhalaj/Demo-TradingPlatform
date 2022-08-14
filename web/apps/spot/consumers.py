from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.layers import get_channel_layer
from core.trade import Trade
from exchange.models import TradeHistory
from limit_order.models import LimitOrders
from itertools import chain
from operator import attrgetter



class TradeConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]

        await self.accept()


    async def receive_json(self, content, **kwargs):
        channel = get_channel_layer()

        result = await self.trade(content)
        try:
            tradeResponse, tradeResult, updatedAsset = result        
            await channel.group_send(
                f"{self.user}_asset", 
                {"type": "send.data", "content": updatedAsset}
            )
            await channel.group_send(
                "recents", 
                {"type": "send.data", "content": tradeResult}
            )
            await channel.group_send(
                f"{self.user}_histories", 
                {"type": "send.data", "content": tradeResult}
            )
        except ValueError:
            tradeResponse = result

        await self.send_json(tradeResponse)


    async def disconnect(self, code):
        self.close()


    async def send_data(self, event):
        data = event["content"]
        await self.send_json(data)
        
       
    @database_sync_to_async
    def trade(self, content):
        tradeObject = Trade(self.user, content)
        result = tradeObject.spotTrade()

        return result



class HistoriesConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.unicastName = f"{self.user}_histories"

        if self.user.is_authenticated:
            await (self.channel_layer.group_add)(self.unicastName, self.channel_name)

        await self.accept()


    async def receive_json(self, content, **kwargs):
        await self.send_json(await self.get_histories(content.get("page")))
       

    async def disconnect(self, code):
        self.channel_layer.group_discard("unicastName", self.channel_name)
        self.close()


    async def send_data(self, event):
        data = event["content"]     
       
        await self.send_json(data)


    @database_sync_to_async
    def get_histories(self, page):
        if page:
            combinedObj = TradeHistory.objects.filter(
                usr=self.user
            ).order_by("-time")[(page-1) * 10 : page * 10]
        else:
            combinedObj = sorted(chain(
                TradeHistory.objects.filter(usr=self.user),
                LimitOrders.objects.filter(usr=self.user)
            ),key=attrgetter('time'))

            if len(combinedObj) > 10:
                combinedObj = combinedObj[len(combinedObj)-10:]

        result = dict()
        for index, item in enumerate(list(combinedObj)):
            result[str(index)] = {
                "type": item.type,
                "pair": item.pair,
                "pairPrice": item.pairPrice,
                "amount": item.amount,
                "datetime": item.time.strftime("%Y/%m/%d %H:%M"),
                "newHistory": False,
            }
            try:
                result[str(index)]["orderType"] = item.orderType
                result[str(index)]["complete"] = item.complete
            except Exception as e:
                result[str(index)]["orderType"] = "limit"
                result[str(index)]["complete"] = False
               
        return result


class RecentsConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.broadcastName = "recents"

        if self.user.is_authenticated:
            await (self.channel_layer.group_add)(self.broadcastName, self.channel_name)

        await self.accept()


    async def receive_json(self, content, **kwargs):
        currentPair = content.get("currentPair")
        await self.send_json(await self.get_recentTrades(currentPair))


    async def disconnect(self, code):
        self.channel_layer.group_discard("broadcastName", self.channel_name)
        self.close()


    async def send_data(self, event):
        data = event["content"]
        await self.send_json(data)


    @database_sync_to_async
    def get_recentTrades(self, pair):
        histObj = TradeHistory.objects.filter(pair=pair).order_by("time")

        if len(histObj) > 10:
            histObj = histObj[len(histObj)-10:]

        result = dict()
        for index, item in enumerate(list(histObj)):
            result[str(index)] = {
                "type": item.type,
                "pairPrice": item.pairPrice,
                "amount": item.amount,
                "pair": pair,
                "time": item.time.strftime("%H:%M:%S"),
            }
        
        return result