from django.contrib.auth.models import AbstractUser
from django.db import models

from api_yamdb.constants import ADMIN, AUTHENTICATED_USER, MODERATOR


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='email')
    confirmation_code = models.CharField(max_length=6, blank=True, null=True)

    ROLE_CHOICES = [
        (AUTHENTICATED_USER, 'Authenticated User'),
        (MODERATOR, 'Moderator'),
        (ADMIN, 'Admin'),
    ]
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='user'
    )
    bio = models.TextField(
        blank=True,
        verbose_name='О себе'
    )

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_admin(self):
        return self.is_superuser or self.role == ADMIN

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.username
