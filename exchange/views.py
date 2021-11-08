from django.shortcuts import render

# Create your views here.
def home(request):
	return render(request, 'exchange/index.html')


def signUp(request):
	return render(request, 'registration/signup.html')

def markets(request):
	return render(request, 'exchange/markets.html')

def symbolInfo(request):
	return render(request, 'exchange/symbol-info.html')

def heatMap(request):
	return render(request, 'exchange/heatmap.html')

def messages(request):
	context = {
		'title' : 'Test',
		'redirect' : 'login',
		'message' : 'Succesfull',
	}
	return render(request, 'registration/messages.html', context=context)