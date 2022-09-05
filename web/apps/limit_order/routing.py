from django.urls import path

from .consumers import LimitConsumer

app_name = "limit_order_ws"
websocket_urlpatterns = [
    path("ws/limit/", LimitConsumer.as_asgi()),
]
