from django.apps import AppConfig


class AnnounConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'announ'

    def ready(self):
        import announ.signals
