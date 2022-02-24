from django.urls import path

from account import consumers

app_name = 'account_ws'
websocket_urlpatterns = [
    path('ws/', consumers.MarketConsumer.as_asgi()),
]