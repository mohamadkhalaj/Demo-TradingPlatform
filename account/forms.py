from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User
from django.contrib.auth.forms import AuthenticationForm
from hcaptcha.fields import hCaptchaField

class LoginForm(AuthenticationForm):
    hcaptcha = hCaptchaField()
    class Meta:
        model = User
        fields = '__all__'


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200)
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')