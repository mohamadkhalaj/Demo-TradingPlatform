from django.urls import path

from .views import Profile, trade_history, wallet

app_name = "account"
urlpatterns = [
    path("wallet/", wallet, name="wallet"),
    path("wallet/<int:page>", wallet, name="wallet"),
    path("trade-history/", trade_history, name="tradeHistory"),
    path("trade-history/", trade_history, name="tradeHistory"),
    path("profile/", Profile.as_view(), name="profile"),
]
