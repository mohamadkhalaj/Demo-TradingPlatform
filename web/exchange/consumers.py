from channels.generic.websocket import AsyncJsonWebsocketConsumer
from .trade import Trade
from .models import TradeHistory
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync

# api, recent-trades and histories all in one
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
        # print('content:', content)
        self.header = content['header']

        if self.header == 'attribs':
            self.current_pair = content['current_pair']
            self.page = content['page']
            await self.initialFillings()

        elif self.header == 'trade_request':
            self.pair = content['pair']
            self.orderType = content['orderType']
            result = await self.trade(content)
            # print('result: ', result)
            trade_response = {'header': 'trade_response', 'state': result['state']}
            await self.channel_layer.group_send(
            self.unicastName,
                {
                    'type': 'send.data',
                    'content': trade_response
                }
            )
            # successful trade
            if result['state'] == 0:
                hist_response = {
                    'header': 'hist_response',
                    'type': result['type'],
                    'pair': self.pair,
                    'amount': result['amount'],
                    'price': result['price'],
                    'orderType': self.orderType,
                    'date': result['date'],
                    'pairPrice': result['pairPrice']
                    }
                await self.channel_layer.group_send(
                    self.unicastName,
                    {
                        'type': 'send.data',
                        'content': hist_response
                    }
                )
                recentTrades_response = {
                    'header': 'recent_response',
                    'type': result['type'],
                    'pair': result['pair'],
                    'price': result['pairPrice'],
                    'amount': result['amount'],
                    'time': result['time']
                    }
                await self.channel_layer.group_send(
                    self.broadcastName,
                    {
                        'type': 'send.data',
                        'content': recentTrades_response
                    }
                )

    async def disconnect(self, code):
        self.channel_layer.group_discard

    
    async def send_data(self, event):
        data = event['content']
        # print('data:', data)
        await self.send_json(data)

    # api call
    @database_sync_to_async
    def trade(self, content):
        if self.header == 'trade_request' and self.orderType == 'market':
            tradeObject = Trade(self.user, self.orderType, content['type'], content['pair'], content['amount'])
            result = tradeObject.result

            return result

    # fill recents and histories after page loaded
    @database_sync_to_async
    def initialFillings(self):
        histObj = TradeHistory.objects.all().order_by('-time')
        counter = 0

        for item in histObj.iterator():
            pair = item.pair.replace('-', '').upper()
            if item.usr == self.user:
                hist_content = {
                    'header': 'hist_response',
                    'type': item.type, 'pair': item.pair, 
                    'pairPrice': item.pairPrice, 'amount': item.amount, 
                    'date': item.time.strftime("%Y:%m:%d:%H:%M"), 
                    'price': item.price
                    }          
                async_to_sync (self.channel_layer.group_send)(
                    self.unicastName,
                    {
                        'type': 'send.data',
                        'content': hist_content
                    }
                )
            if pair == self.current_pair and counter <= 5:
                recent_content = {
                    'header': 'recent_response', 
                    'type': item.type, 'pair': pair, 
                    'price': item.pairPrice, 
                    'amount': item.amount, 
                    'time': item.time.strftime("%H:%M:%S")
                    }
                async_to_sync (self.channel_layer.group_send)(
                    self.unicastName,
                    {
                        'type': 'send.data',
                        'content': recent_content
                    }
                )
            counter += 1