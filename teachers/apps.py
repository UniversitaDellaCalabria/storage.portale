from django.apps import AppConfig


class TeachersConfig(AppConfig):
    name = "teachers"
    verbose_name = "Teachers"

    def ready(self):
        from .management import signals  # noqa: F401
