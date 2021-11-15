from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from .forms import LoginForm, forms, SignupForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

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


class Register(CreateView):
	form_class = SignupForm
	template_name = 'registration/signup.html'

	def form_valid(self,form):
		user = form.save(commit=False)
		user.is_active = False
		user.save()
		current_site = get_current_site(self.request)
		mail_subject = 'Activate your Trading-Platform account.'
		message = render_to_string('registration/activate_account.html', {
			'user': user,
			'domain': current_site.domain,
			# 'uid':urlsafe_base64_encode(force_bytes(user.pk)),
			'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
			'token':account_activation_token.make_token(user),
		})
		to_email = form.cleaned_data.get('email')
		email = EmailMessage(
					mail_subject, message, to=[to_email]
		)
		email.send()
		return HttpResponse('Please confirm your email address to complete the registration')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # login(request, user)
        # # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')