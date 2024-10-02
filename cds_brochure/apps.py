from django.apps import AppConfig


class CdsBrochureConfig(AppConfig):
    name = "cds_brochure"
    verbose_name = "Courses of Study Brochure"

    def ready(self):
        from .management import signals  # noqa: F401
