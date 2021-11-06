from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required

@login_required
def wallet(request):
	return render(request, 'registration/wallet.html')


@login_required
def profile(request):
	return render(request, 'registration/profile.html')


@login_required
def settings(request):
	return render(request, 'registration/settings.html')

@login_required
def trade(request):
	return render(request, 'registration/trade.html')