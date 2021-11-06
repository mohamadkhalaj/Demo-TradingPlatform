from django.contrib.auth import views
from django.urls import path
from .views import wallet, settings, profile, trade

app_name = 'account'
urlpatterns = [
	path('wallet/', wallet, name='wallet'),
	path('settings/', settings, name='settings'),
	path('profile/', profile, name='profile'),
	path('trade/', trade, name='trade'),
]