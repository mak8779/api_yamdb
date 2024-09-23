from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
    verbose_name = 'Отзывы'

    def ready(self):
        from .setup_roles import setup_roles
        setup_roles()
