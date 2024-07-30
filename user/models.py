from django.contrib.auth.models import AbstractUser
from django.db import models


class Permission(models.Model):
    level = models.PositiveIntegerField(unique=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return f"Level {self.level}: {self.description}"

    class Meta:
        verbose_name = 'permission'
        verbose_name_plural = 'permissions'
        db_table = 'permission'


class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_email_verified = models.BooleanField(default=False)
    permission = models.ForeignKey(Permission, on_delete=models.SET_NULL, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        db_table = 'user'

    def __str__(self):
        return self.email
