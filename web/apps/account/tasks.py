from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode

try:
    from django.utils.encoding import force_bytes, force_text
except ImportError:
    from django.utils.encoding import force_str as force_text

from celery import shared_task

from account.tokens import account_activation_token

from .models import User


@shared_task()
def send_activation_code_email(current_site, email_address, user_id):
    user = User.objects.get(pk=user_id)
    mail_subject = "Activate your Trading-Platform account."
    message = render_to_string(
        "registration/activate_account.html",
        {
            "user": user,
            "domain": current_site,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": account_activation_token.make_token(user),
        },
    )
    to_email = email_address
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.content_subtype = "html"
    email.send()
