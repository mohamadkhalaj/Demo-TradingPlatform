from django.contrib.auth import views
from django.urls import path
from .views import (
		home, 
		signUp, 
		markets, 
		symbolInfo, 
		heatMap, 
		trade, 
		portfolio, 
		tradinghistory,
	)

app_name = 'exchange'
urlpatterns = [
	path('', home, name='home'),
	path('markets/', markets, name='markets'),
	path('markets/<int:page>', markets, name='markets'),
	path('symbolInfo/', symbolInfo, name='symbolInfo'),
	path('heatMap/', heatMap, name='heatMap'),
	path('trade/<str:value>', trade, name='trade'),
	path('portfolio/', portfolio, name='portfolio'),
	path('tradinghistory/', tradinghistory, name='tradinghistory'),
]