from django.contrib.auth import views
from django.urls import path
from .views import home, signUp, markets, symbolInfo, heatMap, messages, trade, portfolio, tradinghistory

app_name = 'exchange'
urlpatterns = [
	path('', home, name='home'),
	path('signUp/', signUp, name='signUp'),
	path('markets/', markets, name='markets'),
	path('symbolInfo/', symbolInfo, name='symbolInfo'),
	path('heatMap/', heatMap, name='heatMap'),
	path('messages/', messages, name='messages'),
	path('trade/<str:value>', trade, name='trade'),
	path('portfolio/', portfolio, name='portfolio'),
	path('tradinghistory/', tradinghistory, name='tradinghistory'),
]