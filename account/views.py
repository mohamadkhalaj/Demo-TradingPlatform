from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from exchange.common_functions import search, pretify
from django.contrib.auth import login, authenticate
from exchange.models import Portfolio, TradeHistory
from django.template.loader import render_to_string
from .forms import LoginForm, forms, ProfileForm
from django.contrib.auth.views import LoginView
from .forms import LoginForm, forms, SignupForm
from django.shortcuts import redirect, render
from django.shortcuts import render, redirect
from .tokens import account_activation_token
from django.views.generic import UpdateView
from django.views.generic import CreateView
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .models import User
import requests


class Profile(LoginRequiredMixin, UpdateView):
	model = User
	form_class = ProfileForm
	template_name = 'registration/profile.html'
	success_url = reverse_lazy('account:profile')

	def get_object(self):
		return User.objects.get(pk = self.request.user.pk)

@login_required
def wallet(request):
	total = float()
	portfolio = Portfolio.objects.filter(usr=request.user)
	history = TradeHistory.objects.filter(usr=request.user)

	for index, item in enumerate(portfolio):
		usdt = calc_equivalent(item.cryptoName, 'USDT', item.amount)[1]
		portfolio[index].equivalentAmount = pretify(usdt)
		total += usdt

	context = {
		'portfolio' : portfolio,
		'history' : history,
		'total' : pretify(total),
	}
	print(context)
	return render(request, 'registration/wallet.html', context=context)

@login_required
def settings(request):
	return render(request, 'registration/settings.html')

def trade(request, pair='BINANCE:BTCUSDT'):

	url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=USD&order=market_cap_desc&per_page=250&page=1&sparkline=false'
	data = requests.get(url).json()

	for item in data:
		item['current_price'] = pretify(item['current_price'])

		try:
			item['price_change_percentage_24h'] = float(pretify(item['price_change_percentage_24h']))
		except:
			item['price_change_percentage_24h'] = pretify(item['price_change_percentage_24h'])

	if request.user.is_authenticated:
		portfolio = Portfolio.objects.filter(usr=request.user)
		history = TradeHistory.objects.filter(usr=request.user)
	else:
		portfolio = list()
		history = list()
	
	recentTrades = TradeHistory.objects.all()

	if pair != 'BINANCE:BTCUSDT':
		name = pair.split('-')[0]
		pair = search(pair)
	else:
		name = 'BTC'

	if not pair:
		pair = 'BINANCE:BTCUSDT'
		name = 'BTC'

	context = {
		'pair' : pair,
		'name' : name,
		'history' : history,
		'Portfolio' : portfolio,
		'data' : data,
		'recentTrades' : recentTrades,
	}

	if not pair:
		return redirect('account:trade/BTC-USDT')
	else:
		return render(request, 'registration/trade.html', context=context)


def calc_equivalent(base, qoute, amount):
	response = requests.get("https://min-api.cryptocompare.com/data/pricemulti?fsyms=" + base + "," + qoute + "&tsyms=USDT,USDT")
	response = response.json()
	basePrice = float(response[base]['USDT'])
	qoutePrice = float(response[qoute]['USDT'])
	pairPrice = basePrice / qoutePrice
	equivalent = pairPrice * amount

	return pairPrice, equivalent

class Login(LoginView):
	form_class = LoginForm
	redirect_authenticated_user = True


class Register(CreateView):
	form_class = SignupForm
	template_name = 'registration/signup.html'

	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('exchange:home')
		return super(Register, self).get(request, *args, **kwargs)

	def form_valid(self,form):
		user = form.save(commit=False)
		user.is_active = False
		user.save()
		current_site = get_current_site(self.request)
		mail_subject = 'Activate your Trading-Platform account.'
		message = render_to_string('registration/activate_account.html', {
			'user': user,
			'domain': current_site.domain,
			'uid':urlsafe_base64_encode(force_bytes(user.pk)),
			'token':account_activation_token.make_token(user),
		})
		to_email = form.cleaned_data.get('email')
		email = EmailMessage(
					mail_subject, message, to=[to_email]
		)
		email.send()
		
		context = {
			'title' : 'Signup',
			'redirect' : 'exchange:home',
			'message' : 'Please confirm your email address to complete the registration.',
		}
		return render(self.request, 'registration/messages.html', context=context)

def activate(request, uidb64, token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None
	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.save()
		# allocate 1000 USDT to the new user
		allocate_USDT(user)
		context = {
			'title' : 'Signup',
			'redirect' : 'login',
			'message' : 'Your account has been successfully activated now you can login.',
		}
		return render(
			request, 'registration/messages.html', context=context)
	else:
		context = {
			'title' : 'Signup',
			'redirect' : 'signUp',
			'message' : 'This link has been expired.',
		}
		return render(
			request, 'registration/messages.html', context=context)


def allocate_USDT(user):
	newObj = Portfolio(usr=user, cryptoName='USDT', amount=1000.0, equivalentAmount=None)
	newObj.save()
