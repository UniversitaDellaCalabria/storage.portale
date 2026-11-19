from django.apps import AppConfig


class LaboratoriesNewConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "laboratories_new"

    def ready(self):
        # registra i receiver per la pulizia dei file logo
        from .management import signals  # noqa: F401
