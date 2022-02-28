from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
	email = models.EmailField(unique=True)
	first_login = models.BooleanField(default=True)
	pnlUUID = models.CharField(max_length=50, default=0)
	assetUUID = models.CharField(max_length=50, default=0)