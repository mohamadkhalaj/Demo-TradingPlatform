from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from exchange.models import Portfolio

from .models import User


@receiver(post_save, sender=User)
def create_portfolio(sender, instance, created, **kwargs):
    if created:
        Portfolio.objects.create(usr=instance, cryptoName="USDT", amount=settings.DEFAULT_BALANCE)


@receiver(post_save, sender=User)
def save_portfolio(sender, instance, **kwargs):
    try:
        instance.portfolio.save()
    except:
        pass
