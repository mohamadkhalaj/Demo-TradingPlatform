from django.urls import path

from exchange import consumers

app_name = 'exchange_ws'
websocket_urlpatterns = [
    path('ws/trade/', consumers.TradeConsumer.as_asgi()),
    path('ws/trade/', consumers.PriceConsumer.as_asgi()),
]