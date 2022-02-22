from django.urls import path

from exchange import consumers

app_name = 'exchange_ws'
websocket_urlpatterns = [
    # path('ws/chat/<str:chat_id>/', consumers.ChatConsumer),
]