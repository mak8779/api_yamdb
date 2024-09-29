from django.apps import AppConfig
from django.db.models.signals import post_migrate


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
    verbose_name = 'Отзывы'

    def ready(self):
        from .setup_roles import setup_roles
        post_migrate.connect(setup_roles, sender=self)
