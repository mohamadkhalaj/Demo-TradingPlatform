from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.layers import get_channel_layer
from core.trade import Trade
from exchange.models import TradeHistory



class TradeConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.unicastName = f"{self.user}_unicast"

        if self.user.is_authenticated:
            await (self.channel_layer.group_add)(self.unicastName, self.channel_name)
         

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
                f"{self.user}_recents", 
                {"type": "send.data", "content": tradeResult}
            )
            await channel.group_send(
                f"{self.user}_histories", 
                {"type": "send.data", "content": tradeResult}
            )
        except ValueError:
            tradeResponse = result

        await self.channel_layer.group_send(
                self.unicastName, 
                {"type": "send.data", 
                "content": tradeResponse}
        )


    async def disconnect(self, code):
        self.channel_layer.group_discard("unicastName", self.channel_name)


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


    async def send_data(self, event):
        data = event["content"]     
       
        await self.send_json(data)


    @database_sync_to_async
    def get_histories(self, page):
        if page:
            histObj = TradeHistory.objects.filter(usr=self.user).order_by("-time")[(page-1) * 10 : page * 10]
        else:
            histObj = TradeHistory.objects.filter(usr=self.user).order_by("time")
            if len(histObj) > 10:
                histObj = histObj[len(histObj)-10:]

        result = dict()
        for index, item in enumerate(list(histObj)):
            result[str(index)] = {
                    "type": item.type,
                    "pair": item.pair,
                    "pairPrice": item.pairPrice,
                    "amount": item.amount,
                    "datetime": item.time.strftime("%Y/%m/%d-%H:%M"),
                    "orderType": item.orderType,
                    "complete": item.complete,
                    "newHistory": False,
                }

        return result


class RecentsConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.unicastName = f"{self.user}_recents"

        if self.user.is_authenticated:
            await (self.channel_layer.group_add)(self.unicastName, self.channel_name)

        await self.accept()


    async def receive_json(self, content, **kwargs):
        currentPair = content.get("currentPair")
        await self.send_json(await self.get_recentTrades(currentPair))


    async def disconnect(self, code):
        self.channel_layer.group_discard("unicastName", self.channel_name)


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