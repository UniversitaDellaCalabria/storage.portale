from django.apps import AppConfig


class LaboratoriesConfig(AppConfig):
    name = "laboratories"
    verbose_name = "Laboratories"

    def ready(self):
        from .management import signals  # noqa: F401
