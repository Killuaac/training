from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    fio = models.CharField(max_length=128)
    username = models.CharField(max_length=128)
    password = models.CharField(max_length=128,
                                validators=[MinLengthValidator(8)])

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fio', 'username', 'password']
