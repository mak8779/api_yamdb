from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='email')
    confirmation_code = models.CharField(max_length=6, blank=True, null=True)

    ROLE_CHOICES = [
        ('user', 'Authenticated User'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='user'
    )

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    @property
    def is_admin(self):
        return self.is_superuser or self.role == 'admin'

    def __str__(self):
        return self.username
