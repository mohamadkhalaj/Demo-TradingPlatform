from django.urls import path

from .views import exchange_trade, markets, search_cryptos

app_name = "exchange"
urlpatterns = [
    path("markets/", markets, name="markets"),
    path("search/<str:value>", search_cryptos, name="search"),
    path("trade/<str:pair>", exchange_trade, name="exchange_trade"),
    path("trade/", exchange_trade, name="exchange_trade"),
]
