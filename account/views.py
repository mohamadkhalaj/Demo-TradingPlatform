from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, forms

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

class Login(LoginView):
	form_class = LoginForm
	redirect_authenticated_user = True