from django.urls import path

from account import consumers

app_name = "account_ws"
websocket_urlpatterns = [
    path("ws/", consumers.MarketConsumer.as_asgi()),
    path("ws/wallet/", consumers.WalletSocket.as_asgi()),
    path("ws/wallet/chart/", consumers.ChartSocket.as_asgi()),
]
