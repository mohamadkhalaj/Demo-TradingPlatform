from django.contrib.auth import views
from django.urls import path
from .views import test

app_name = 'account'
urlpatterns = [
	path('test', test, name='test')
]