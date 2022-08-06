from django.urls import path

from . import consumers

app_name = "exchange_ws"
websocket_urlpatterns = [
    path("ws/", consumers.MarketConsumer.as_asgi()),
    path("ws/trade/asset/", consumers.AssetConsumer.as_asgi()),
]
