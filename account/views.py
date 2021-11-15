from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView
from .forms import LoginForm, forms, ProfileForm
from django.urls import reverse_lazy
from .models import User

class Profile(LoginRequiredMixin, UpdateView):
	model = User
	form_class = ProfileForm
	template_name = 'registration/profile.html'
	success_url = reverse_lazy('account:profile')

	def get_object(self):
		return User.objects.get(pk = self.request.user.pk)

@login_required
def wallet(request):
	return render(request, 'registration/wallet.html')

@login_required
def settings(request):
	return render(request, 'registration/settings.html')

@login_required
def trade(request):
	return render(request, 'registration/trade.html')

class Login(LoginView):
	form_class = LoginForm
	redirect_authenticated_user = True