from django.contrib.auth import views
from django.urls import path
from .views import wallet, tradeHistory, Profile, trade

app_name = 'account'
urlpatterns = [
	path('wallet/', wallet, name='wallet'),
	path('wallet/<int:page>', wallet, name='wallet'),
	path('tradeHistory/', tradeHistory, name='tradeHistory'),
	path('tradeHistory/<int:page>', tradeHistory, name='tradeHistory'),
	path('profile/', Profile.as_view(), name='profile'),
	path('trade/<str:pair>', trade, name='trade'),
	path('trade/', trade, name='trade'),
]