from django.apps import AppConfig


class NportalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'nportal'

    def ready(self):
        import nportal.signals