from django.shortcuts import render
from django.contrib.auth.views import LoginView

def test(request):
	return render(request, 'account/test.html')


	