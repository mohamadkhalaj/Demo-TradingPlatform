import asyncio

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from core.charts import Charts
from core.utils import calc_equivalent, get_crypto_compare, pretify
from django.db.models import Sum
from exchange.models import Portfolio, TradeHistory
from limit_order.models import LimitOrders


class ChartSocket(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_authenticated:
            await self.accept()
        else:
            self.close()

    async def send_data(self):
        portfolio = await self.get_portfolio()
        trades = await self.get_trades()

        dictionary = {}

        # orderMargin = await self.get_orders()
        chart = Charts(portfolio, trades)
        assetAllocation = chart.asset_allocation()
        pnl = chart.profit_loss()

        dictionary["assetAllocation"] = assetAllocation
        dictionary["pnl"] = pnl

        await self.send_json(dictionary)
        await asyncio.sleep(60)

    async def disconnect(self, close_code):
        self.close()

    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            while True:
                await asyncio.ensure_future(self.send_data())

    @database_sync_to_async
    def get_portfolio(self):
        return list(
            Portfolio.objects.all().filter(
                usr=self.user,
                marketType="spot",
            )
        )

    @database_sync_to_async
    def get_trades(self):
        return list(
            TradeHistory.objects.all().filter(
                usr=self.user,
                complete=True,
            )
        )

    @database_sync_to_async
    def get_orders(self):
        return (
            LimitOrders.objects.all()
            .filter(
                usr=self.user,
                amount__gt=0,
            )
            .aggregate(Sum("price"))["price__sum"]
        )


class WalletSocket(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_authenticated:
            await self.accept()
        else:
            self.close()

    async def send_data(self):
        domain = "https://cryptocompare.com"

        cryptocompare = get_crypto_compare()
        portfolio = await self.get_portfolio()
        dictionary = {}
        totalMargin = sum([calc_equivalent(item.cryptoName, "USDT", item.amount)[1] for item in portfolio])

        assets = {}
        for item in portfolio:
            assets[item.cryptoName] = float(item.amount)

        array = []
        data = cryptocompare.get_price(list(assets.keys()), currency="USD", full=True)["RAW"]

        for item in data:
            tmp = data[item]["USD"]
            price = float(tmp["PRICE"])
            total = price * assets[item]
            sym = await self.get_symbol_form_db(item, total)
            array.append(
                {
                    "symbol": item,
                    "amount": assets[item],
                    "total": total,
                    "img": domain + tmp["IMAGEURL"],
                }
            )

        availableMargin = await self.get_orders()
        # dictionary["total"] = pretify(totalMargin + availableMargin)
        dictionary["total"] = None
        dictionary["assets"] = array
        dictionary["available"] = pretify(totalMargin)

        await self.send_json(dictionary)
        await asyncio.sleep(1)

    async def disconnect(self, close_code):
        self.close()

    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            while True:
                await asyncio.ensure_future(self.send_data())

    @database_sync_to_async
    def get_portfolio(self):
        return list(
            Portfolio.objects.all()
            .filter(
                usr=self.user,
                marketType="spot",
                amount__gt=0,
            )
            .order_by("-equivalentAmount")
        )

    @database_sync_to_async
    def get_orders(self):
        return (
            LimitOrders.objects.all()
            .filter(
                usr=self.user,
                amount__gt=0,
            )
            .aggregate(Sum("price"))["price__sum"]
        )

    @database_sync_to_async
    def get_symbol_form_db(self, symbol, total):
        sym = Portfolio.objects.get(
            usr=self.user,
            marketType="spot",
            cryptoName=symbol,
        )
        sym.equivalentAmount = total
        sym.save()


class HistoriesConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.unicastName = f"{self.user}_HSTunicast"

        if self.user.is_authenticated:
            await (self.channel_layer.group_add)(self.unicastName, self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def receive_json(self, content, **kwargs):
        page = content["page"]
        result = await self.initialFilling(page)
        await self.send_json(result)

    async def disconnect(self, code):
        pass

    async def send_data(self, event):
        data = event["content"]
        await self.send_json(data)

    @database_sync_to_async
    def initialFilling(self, page):

        before = (page - 1) * 10
        after = page * 10
        histObj = TradeHistory.objects.filter(usr=self.user).order_by("-id")[before:after]

        hist_content = dict()

        for index, item in enumerate(histObj):
            hist_content[str(index)] = {
                "header": "hist_responses",
                "type": item.type,
                "pair": item.pair,
                "pairPrice": item.pairPrice,
                "amount": item.amount,
                "date": item.time.strftime("%Y-%m-%d:%H:%M"),
                "price": item.price,
            }

        return hist_content
