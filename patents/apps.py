from django.apps import AppConfig


class PatentsConfig(AppConfig):
    name = "patents"
    verbose_name = "Patents"

    def ready(self):
        from .management import signals  # noqa: F401
