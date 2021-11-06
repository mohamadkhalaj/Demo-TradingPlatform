from django.contrib.auth import views
from django.urls import path
from .views import home

app_name = 'exchange'
urlpatterns = [
	path('', home, name='home')
]