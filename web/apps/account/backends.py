from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from .models import User


class EmailOrUsernameModelBackend(ModelBackend):
    """
    This is a ModelBacked that allows authentication
    with either a username or an email address.

    """

    def get_user(self, username):
        try:
            return get_user_model().objects.get(pk=username)
        except get_user_model().DoesNotExist:
            return None

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)
        if "@" in username:
            kwargs = {"email": username}
        else:
            kwargs = {"username": username}
        if username is None or password is None:
            return
        try:
            # filter user case insensitively
            temp = self.case_insensitive_username(kwargs)
            kwargs = temp
            print(kwargs)
            user = User._default_manager.filter(**kwargs).get()
        except User.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            User().set_password(password)
        else:
            if user.check_password(password) and super().user_can_authenticate(user):
                return user

    def case_insensitive_username(self, kwargs):
        temp = {}
        for key in kwargs.keys():
            print(key)
            temp[key + "__iexact"] = kwargs[key]
        return temp
