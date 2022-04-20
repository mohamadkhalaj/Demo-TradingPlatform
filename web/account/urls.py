from django.contrib.auth import views
from django.urls import path

from .views import Profile, trade, tradeHistory, wallet

app_name = "account"
urlpatterns = [
    path("wallet/", wallet, name="wallet"),
    path("wallet/<int:page>", wallet, name="wallet"),
    path("tradeHistory/", tradeHistory, name="tradeHistory"),
    path("tradeHistory/", tradeHistory, name="tradeHistory"),
    path("profile/", Profile.as_view(), name="profile"),
    path("trade/<str:pair>", trade, name="trade"),
    path("trade/", trade, name="trade"),
]
