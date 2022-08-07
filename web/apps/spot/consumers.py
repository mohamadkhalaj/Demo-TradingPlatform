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
        self.broadcastName = "broadcast"

        await (self.channel_layer.group_add)(self.broadcastName, self.channel_name)
        if self.user.is_authenticated:
            await (self.channel_layer.group_add)(self.unicastName, self.channel_name)
         

        await self.accept()


    async def receive_json(self, content, **kwargs):
        channel = get_channel_layer()

        if content.get("currentPair"):
            self.currentPair = content.get("currentPair")
            await channel.group_send(
                f"{self.user}_asset",
                {"type": "send.data", "content": await self.get_assetAmount()},
            )
            await self.send_json(await self.get_recentTrades())

        else:
            result = await self.trade(content)   
            try:
                tradeResponse, tradeResult, executedTime = result        
                await channel.group_send(
                    f"{self.user}_asset", 
                    {"type": "send.data", "content": await self.get_assetAmount()}
                )
                tradeResult["0"]["time"] = executedTime.strftime("%H:%M:%S")
                await self.channel_layer.group_send(
                    self.broadcastName, 
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
        self.channel_layer.group_discard("broadcastName", self.channel_name)


    async def send_data(self, event):
        data = event["content"]
        await self.send_json(data)
        
       
    @database_sync_to_async
    def trade(self, content):
        tradeObject = Trade(self.user, content)
        result = tradeObject.spotTrade()

        return result


    @database_sync_to_async
    def get_assetAmount(self):
        currencies = [self.currentPair.split('-')[0], self.currentPair.split('-')[1]]
        result = dict()
        
        for index, currency in enumerate(currencies):
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


    @database_sync_to_async
    def get_recentTrades(self):
        histObj = TradeHistory.objects.filter(
            usr=self.user, 
            pair=self.currentPair
            ).order_by("time")

        if len(histObj) > 10:
            histObj = histObj[len(histObj)-10:]

        result = dict()
        for index, item in enumerate(list(histObj)):
            result[str(index)] = {
                        "type": item.type,
                        "pair": self.currentPair,
                        "pairPrice": item.pairPrice,
                        "amount": item.amount,
                        "time": item.time.strftime("%H:%M:%S"),
                    }

        return result