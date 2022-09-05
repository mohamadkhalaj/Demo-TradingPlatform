from django.urls import path

from . import consumers

app_name = "account_ws"
websocket_urlpatterns = [
    path("ws/wallet/", consumers.WalletSocket.as_asgi()),
    path("ws/wallet/chart/", consumers.ChartSocket.as_asgi()),
    path("ws/histories/", consumers.HistoriesConsumer.as_asgi()),
    path("ws/open-orders/", consumers.OpenOrdersConsumer.as_asgi()),
]
