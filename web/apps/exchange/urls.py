from django.urls import path

from .views import echo, home, markets, portfolio, recentTrades, search, trade, tradinghistory

app_name = "exchange"
urlpatterns = [
    path("", home, name="home"),
    path("markets/", markets, name="markets"),
    path("trade/<str:value>", trade, name="trade"),
    path("portfolio/", portfolio, name="portfolio"),
    path("tradinghistory/", tradinghistory, name="tradinghistory"),
    path("recentTrades/", recentTrades, name="recentTrades"),
    path("echo/", echo, name="echo"),
    path("search/<str:value>", search, name="search"),
]
