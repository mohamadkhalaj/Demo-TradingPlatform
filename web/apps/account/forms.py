import os
import unicodedata

from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    UserCreationForm,
    UsernameField,
)
from django.contrib.auth.validators import ASCIIUsernameValidator

from .models import User

is_production = os.environ.get("DJANGO_SETTINGS_MODULE") == "config.settings.production"
if is_production:
    from hcaptcha.fields import hCaptchaField


class ASCIIUsernameField(UsernameField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validators.append(ASCIIUsernameValidator())


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


def unicode_ci_compare(s1, s2):
    return unicodedata.normalize("NFKC", s1).casefold() == unicodedata.normalize("NFKC", s2).casefold()


class PasswordResetFormAllowNoPassword(PasswordResetForm):
    if is_production:
        hcaptcha = hCaptchaField()

    def get_users(self, email):
        email_field_name = User.get_email_field_name()
        active_users = User._default_manager.filter(
            **{
                "%s__iexact" % email_field_name: email,
                "is_active": True,
            }
        )
        return (u for u in active_users if unicode_ci_compare(email, getattr(u, email_field_name)))


class PasswordChangeFormOauth(PasswordChangeForm):
    if is_production:
        hcaptcha = hCaptchaField()

    def clean_old_password(self):
        if not self.user.has_usable_password():
            # generate random password
            old_password = User.objects.make_random_password()
            self.user.set_password(old_password)
            self.user.save(update_fields=["password"])
            return old_password
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages["password_incorrect"],
                code="password_incorrect",
            )
        return old_password


class SignupForm(UserCreationForm):
    if is_production:
        hcaptcha = hCaptchaField()
    email = forms.EmailField(max_length=200)

    def clean(self):
        cleaned_data = super(SignupForm, self).clean()
        username = cleaned_data.get("username")
        if username and User.objects.filter(username__iexact=username).exists():
            self.add_error("username", "A user with that username already exists.")
        return cleaned_data

    class Meta:
        model = User
        field_classes = {"username": ASCIIUsernameField}
        fields = ("username", "email", "password1", "password2")
