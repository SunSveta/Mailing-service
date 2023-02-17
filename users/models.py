from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

NULLABLE = {'blank': True, 'null': True}

class CustomUserManager(UserManager):
    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user


class User(AbstractUser):

    objects = CustomUserManager()
    username = None

    email = models.EmailField(verbose_name='почта', unique=True)
    token = models.CharField(max_length=150, verbose_name='токен', **NULLABLE)
    token_expired = models.DateTimeField(**NULLABLE)
    my_password = models.CharField(max_length=100, verbose_name='мой пароль')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        permissions = [
            (
                "change_user_status",
                "Can change user status"
            )
        ]
