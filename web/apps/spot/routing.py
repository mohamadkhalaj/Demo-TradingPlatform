from django.urls import path
from exchange.consumers import MarketConsumer

from .consumers import TradeConsumer

app_name = "spot_ws"
websocket_urlpatterns = [
    path("ws/trade/", TradeConsumer.as_asgi()),
    path("ws/trade/prices/", MarketConsumer.as_asgi()),
]