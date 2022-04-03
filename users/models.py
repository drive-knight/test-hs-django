from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    inviteRegex = RegexValidator(regex=r"^\+?1?\w{6}$")
    code_invite = models.CharField(validators=[inviteRegex], max_length=6, blank=True)
    another_invite = models.CharField(validators=[inviteRegex], max_length=6, blank=True, null=True, default=None)
    phoneRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    phone = models.CharField(validators=[phoneRegex], max_length=16, unique=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.phone

