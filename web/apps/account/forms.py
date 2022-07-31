import os

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User

is_production = os.environ.get("DJANGO_SETTINGS_MODULE") == "config.settings.production"
if is_production:
    from hcaptcha.fields import hCaptchaField


class LoginForm(AuthenticationForm):
    if is_production:
        hcaptcha = hCaptchaField()

    class Meta:
        model = User
        fields = "__all__"


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):

        super(ProfileForm, self).__init__(*args, **kwargs)

        self.fields["username"].help_text = None
        self.fields["username"].disabled = True
        self.fields["email"].disabled = True

        self.fields["username"].widget.attrs["placeholder"] = "Username"
        self.fields["email"].widget.attrs["placeholder"] = "Email"
        self.fields["first_name"].widget.attrs["placeholder"] = "First name"
        self.fields["last_name"].widget.attrs["placeholder"] = "Last name"

        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control p-2 border-3"

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "first_login"]


class SignupForm(UserCreationForm):
    if is_production:
        hcaptcha = hCaptchaField()
    email = forms.EmailField(max_length=200)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "hcaptcha")
