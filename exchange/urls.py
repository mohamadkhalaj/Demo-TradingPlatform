from django.contrib.auth import views
from django.urls import path
from .views import home, signUp, markets, symbolInfo, heatMap

app_name = 'exchange'
urlpatterns = [
	path('', home, name='home'),
	path('signUp/', signUp, name='signUp'),
	path('markets/', markets, name='markets'),
	path('symbolInfo/', symbolInfo, name='symbolInfo'),
	path('heatMap/', heatMap, name='heatMap'),
]