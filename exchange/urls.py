from django.contrib.auth import views
from django.urls import path
from .views import (
		home, 
		signUp, 
		markets,  
		trade, 
		portfolio, 
		tradinghistory,
		recentTrades,
	)

app_name = 'exchange'
urlpatterns = [
	path('', home, name='home'),
	path('markets/', markets, name='markets'),
	path('markets/<int:page>', markets, name='markets'),
	path('trade/<str:value>', trade, name='trade'),
	path('portfolio/', portfolio, name='portfolio'),
	path('tradinghistory/', tradinghistory, name='tradinghistory'),
	path('recentTrades/', recentTrades, name='recentTrades'),
]